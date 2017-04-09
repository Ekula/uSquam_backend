from resources.session.service import SessionService
from resources.task.service import TaskService
from resources.data.service import DataService
from intent import IntentParser
import random

class _IdleInteractionHandler:
    def __init__(self):
        self.handlers = {}

    def interaction(self, intent):
        def decorator(f):
            self.handlers[intent] = f
            return f
        
        return decorator

    def handleInput(self, user_id, message):
        intent = IntentParser.parse(message, self.handlers.keys())
        if not intent:
            return "Sorry, I don't know what to say."
        
        handle_function = self.handlers.get(intent['intent_type'])

        if handle_function:
            return handle_function(user_id, intent)
        else:
            return "Sorry, I don't know what to say."

IdleInteractionHandler = _IdleInteractionHandler()

@IdleInteractionHandler.interaction("Help")
@IdleInteractionHandler.interaction("Greetings")
def help(worker, message):
    return """
    Hi, 

    I am usquam_bot and I am here to help you fulfill small comutation tasks \
    for a reward using the usquam platform. Here's what I can do. 

    I can give you a new task. Just ask me to give you a new task and I will do so, \
    e.g. "Give me a task".
    
    If you need help, just say "I need some help" or "I don't know what to do"
    """

@IdleInteractionHandler.interaction("NewTask")
def newTask(worker, message):
    print 'Received: ', message, ' - Creating new task'
    # If selected task type = 'regular'
    # Choose random task and random item from data collection
    tasks = TaskService.getAll()
    task = random.choice(tasks)

    data_collection = DataService.get(None, task['data_collection_id'])

    task_data = random.choice(data_collection['task_data'])
    new_session = {
        'worker_id': worker['id'],
        'task_id': task['id'],
        'task_data_id': task_data['_id'],
        'review': false
    }
    session = SessionService.insert(new_session)

    question = task['questions'][0]['message']

    # Todo: Create a question format function somewhere (same code in session_interaction_handler)
    # Find question data content
    data_collection = DataService.get(None, task['data_collection_id'])
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

    return answer

@IdleInteractionHandler.interaction("NewReviewTask")
def newReviewTask(worker, message):
    print 'Received: ', message, ' - Creating new review task'
    # if selected task type = 'review'
    # 'session' is the current session for the review task
    # 'reviewed_session' is the session being reviewed
    
    sessions = SessionService.getAll()
    
    # make sure to only generate review tasks for sessions of other workers and those that are not validated yet 
    for item in sessions:
        if (item.validated == False and item.review == False and item.worker_id != worker['id'] ):
            reviewed_session = item
            break
            
    task = TaskService.get(reviewed_session.task_id)
    
    # generate a review task for the selected session and corresponding task
    reviewtask = TaskService.generate_reviewtask(reviewed_session, task)
    
    data_collection = DataService.get(None, task['data_collection_id'])
    
    task_data = random.choice(data_collection['task_data'])
    
    question = task['questions'][0]['message']
    answer = reviewed_session['answers'][0]['message']
    
    # Find question data content
    data_collection = DataService.get(None, task['data_collection_id'])
    task_data = None
    for item in data_collection['task_data']:
        if str(item['_id']) == str(reviewed_session['task_data_id']):
            task_data = item
            break

    # There could be no data item specified for this question
    if 'question_data_idx' in task['questions'][0]:
        # Choose first question data item from the list
        question_data = task_data.question_data[task['questions'][0]['question_data_idx']].content
        review = '{}\n  {}\n {}\n {}'.format(question, question_data, 'Given answer:', answer)
    else:
        review = '{}\n {}\n {}'.format(question, 'Given answer:' , answer)

    return review