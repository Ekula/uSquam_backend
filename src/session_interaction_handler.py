from resources.task.service import TaskService
from resources.session.service import SessionService
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
    task = TaskService.get(session['task_id'])
    state = session['state']

    answer = Answer()
    answer.message = message
    answer.question = task['questions'][state]['_id']
    session.answers.append(answer)

    answer = ''
    if state + 1 < len(task['questions']):
        state += 1
        answer = task['questions'][state]['message']
        session.state = state
        
    else:
        answer = "Thank you for completing the task"
        session.status = "DONE"
    
    SessionService.update(session)
    
    return answer


