from resources.session.service import SessionService
from resources.task.service import TaskService
from resources.data.service import DataService
import random

class _IdleInteractionHandler:

    def __init__(self):
        self.handlers = {}

    def interaction(self, expression):
        def decorator(f):
            self.handlers[expression] = f
            return f
        
        return decorator

    def handleInput(self, user_id, message):
        handle_function = self.handlers.get(message)
        if handle_function:
            return handle_function(user_id, message)
        else:
            return "Sorry, I don't know what to say."

IdleInteractionHandler = _IdleInteractionHandler()

@IdleInteractionHandler.interaction("start")
def start(user_id, message):
    return """Hey what would you like to do?
    
    Just type task to get a new task!
    """

@IdleInteractionHandler.interaction("task")
def newTask(worker, message):
    print 'Received: ', message, ' - Creating new task'
    # Choose random task and random item from data collection
    tasks = TaskService.getAll()
    task = random.choice(tasks)

    data_collection = DataService.get(None, task['data_collection_id'])

    task_data = random.choice(data_collection['task_data'])
    new_session = {
        'worker_id': worker['id'],
        'task_id': task['id'],
        'task_data_id': task_data['_id']
    }
    session = SessionService.insert(new_session)

    question = task['questions'][0]['message']

    # Todo: Create a question format function somewhere (same code in session_interaction_handler)
    # Find question data content
    data_collection = DataService.get(None, task['data_collection_id'])
    task_data = None
    for item in data_collection['task_data']:
        print item['_id'], session['task_data_id']
        if str(item['_id']) == str(session['task_data_id']):
            task_data = item
            break

    # There could be no data item specified for this question
    if task_data is not None:
        # Choose first question data item from the list
        question_data = task_data.question_data[task['questions'][0]['question_data_idx']].content
        answer = '{}\n  {}'.format(question, question_data)
    else:
        answer = '{}'.format(question)

    return answer
