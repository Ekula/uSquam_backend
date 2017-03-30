from resources.task.service import TaskService
from resources.session.service import SessionService
from resources.data.service import DataService
from resources.session.session_model import Answer

class _SessionInteractionHandler:

    def __init__(self):
        self.handlers = {}

    def interaction(self, expression):
        def decorator(f):
            self.handlers[expression] = f
            return f
        
        return decorator

    def handleInput(self, session, message):
        handle_function = self.handlers.get(message)
        if handle_function:
            return handle_function(session, message)
        else:
            handle_function = self.handlers.get('*')
            return handle_function(session, message)

SessionInteractionHandler = _SessionInteractionHandler()

@SessionInteractionHandler.interaction("*")
def newTask(session, message):
    print 'newTask'
    task = TaskService.get(session['task_id'])
    state = session['state']

    answer = Answer()
    answer.message = message
    # answer.question = task['questions'][state]['_id']
    session.answers.append(answer)

    if state + 1 < len(task['questions']):
        state += 1

        # Todo: Create a question format function somewhere (same code in idle_interaction_handler)
        # Find question data content
        data_collection = DataService.get(None, task['data_collection_id'])
        task_data = None
        for item in data_collection['items']:
            print item['_id'], session['task_data_id']
            if str(item['_id']) == str(session['task_data_id']):
                task_data = item
                break
        question_data = task_data.items[task['questions'][state]['question_data_idx']].content

        # Create response to worker answer: New question and the accompanied question data
        question = task['questions'][state]['message']
        answer = '{}\n  {}'.format(question, question_data)
        session.state = state
        
    else:
        answer = "Thank you for completing the task"
        session.status = "DONE"
    
    SessionService.update(session)
    
    return answer


