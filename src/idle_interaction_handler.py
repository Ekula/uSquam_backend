from resources.session.service import SessionService
from resources.task.service import TaskService
from resources.data.service import DataService
from resources.worker.service import WorkerService
from resources.session.session_model import Session
from intent import IntentParser
import random
import logging

class _IdleInteractionHandler:
    def __init__(self):
        self.handlers = {}

    def interaction(self, intent):
        def decorator(f):
            self.handlers[intent] = f
            return f
        
        return decorator

    def handleInput(self, worker, message):
        intent = IntentParser.parse(message, self.handlers.keys())
        error_result = {'answer': "Sorry, I don't know what to say."}
        if not intent:
            return error_result

        handle_function = self.handlers.get(intent['intent_type'])

        if handle_function:
            return handle_function(worker, message, intent)
        else:
            return error_result

IdleInteractionHandler = _IdleInteractionHandler()

############################################################################
# Helper functions
############################################################################

def createTaskInstance(task, session):
    question = task['questions'][0]['message']
    # Todo: Create a question format function somewhere (same code in session_interaction_handler)
    # Find question data content
    data_collection = DataService.get(task['data_collection_id'])
    task_data = None
    for item in data_collection['task_data']:
        if str(item['_id']) == str(session['task_data_id']):
            task_data = item
            break

    # There could be no data item specified for this question
    if 'question_data_idx' in task['questions'][0]:
        # Choose first question data item from the list
        question_data = task_data.question_data[task['questions'][0]['question_data_idx']].content
        answer = '{}\n  {}'.format(question, question_data)
    else:
        answer = '{}'.format(question)

    return {'answer': answer}

def createTaskSessionIntance(worker, task):
    data_collection = DataService.get(task['data_collection_id'])

    task_data = random.choice(data_collection['task_data'])
    new_session = {
        'worker_id': worker['id'],
        'task_id': task['id'],
        'task_data_id': task_data['_id'],
        'review': False
    }
    return SessionService.insert(new_session)

def createReviewSessionIntance(worker, task):
    new_session = {
        'worker_id': worker['id'],
        'task_id': task['id'],
        'type': 'REVIEW',
        'review': False
    }
    return SessionService.insert(new_session)


def createIdleSessionInstance(worker, task):
    new_session = {
        'worker_id': worker['id'],
        'task_id': task['id'],
        'task_data_id': None,
        'type': 'IDLE',
        'review': False
    }
    return SessionService.insert(new_session)

############################################################################
# Interactions
############################################################################


@IdleInteractionHandler.interaction("Help")
@IdleInteractionHandler.interaction("Greetings")
def help(worker, message, intent):
    return {'answer': """
Hi, 

I am usquam_bot and I am here to help you fulfill small commutation tasks \
for a reward using the uSquam platform. Here's what I can do. 

I can give you a new task. Just ask me to give you a new task and I will do so, \
e.g. "Give me a task".

If you need help, just say "I need some help" or "I don't know what to do"
"""}


@IdleInteractionHandler.interaction("TaskList")
def taskList(worker, message, intent):
    tasks = TaskService.getAll()
    task = TaskService.findWhere(name="Select Task")

    answer = "These are the tasks that are currently available: \
 \n\n{}\n\nWhich task would you like?".format("\n".join(["{}".format(task.name) for task in tasks]))

    session = createIdleSessionInstance(worker, task)

    return {'answer': answer}

@IdleInteractionHandler.interaction("Number")
def selectTask(session, message, intent):

    if not 'id' in session or not session['type'] == 'IDLE': 
        return {'answer': 'It seems like you haven\'t listed the tasks first. \
 To select a task, send "tasks". '}

    index = int(intent['NumberKeyword']) - 1
    tasks = TaskService.getAll()

    task = None
    if index < len(tasks):
        task = tasks[index]
    else:
        return {'answer': "Please choose a task from the list by indicating it's number. Say e.g. '1'"}
    
    worker = WorkerService.get(session['worker_id'])

    session.status = "DONE"
    SessionService.update(session)

    new_session = createTaskSessionIntance(worker, task)

    return createTaskInstance(task, new_session)


@IdleInteractionHandler.interaction("NewTask")
def newTask(worker, message, intent):
    print 'Received: ', message, ' - Creating new task'
    # Choose random task and random item from data collection
    tasks = TaskService.getAll()
    task = random.choice(tasks)

    session = createTaskSessionIntance(worker, task)

    return createTaskInstance(task, session)


@IdleInteractionHandler.interaction("NewReviewTask")
def newReviewTask(worker, message, intent):
    print 'Received: ', message, ' - Creating new review task'
    
    sessions = SessionService.getAll()
    
    reviewed_session = None
    for item in sessions:
        if not item.validated and item.type == 'TASK' and item.worker_id != worker['id']:
            reviewed_session = item
            break

    if not reviewed_session:
        return {'answer': "There are currently no tasks that need reviewing."}

    task = TaskService.get(reviewed_session.task_id)
    
    reviewtask = TaskService.generate_reviewtask(reviewed_session, task)    
    question = task['questions'][0]
    answer = reviewed_session['answers'][0]['message']
    
    data_collection = DataService.get(task.data_collection_id)
    task_data = data_collection.task_data.filter(_id=reviewtask.task_data_id).first()

    if 'question_data_idx' in task['questions'][0]:
        question_data = task_data.question_data[question['question_data_idx']].content
        review = '{}\n  {}\n {}\n {}'.format(question['message'], question_data, 'Given answer:', answer)
    else:
        review = '{}\n {}\n {}'.format(question['message'], 'Given answer:' , answer)

    session = createReviewSessionIntance(worker, reviewtask)

    return {'answer': review}