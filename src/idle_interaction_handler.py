from resources.session.service import SessionService
from resources.task.service import TaskService
from resources.data.service import DataService
from resources.worker.service import WorkerService
from resources.session.session_model import Session
from src.helper_functions import *
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

    answer = "These are the tasks that are currently available: \
 \n\n{}\n\nWhich task would you like?".format("\n".join(["{}".format(task.name) for task in tasks]))

    task = TaskService.findIdleTaskWhere(name="SelectTask")

    session = createIdleSessionInstance(worker, task)

    return {'answer': "\n".join([answer, task.states[0].question])}

@IdleInteractionHandler.interaction("NewTask")
def newTask(worker, message, intent):
    print 'Received: ', message, ' - Creating new task'
    # Choose random task and random item from data collection
    tasks = TaskService.getAll()
    task = random.choice(tasks)

    session = createTaskSessionIntance(worker, task)

    return formatQuestion(task, session)


@IdleInteractionHandler.interaction("NewReviewTask")
def newReviewTask(worker, message, intent):
    print 'Received: ', message, ' - Creating new review task'
    
    sessions = SessionService.getAll()
    
    reviewed_session = None
    print worker['id']
    for item in sessions:
        if not item.validated and item.type == 'TASK' and item.status == 'DONE' and item.worker_id != worker['id']:
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