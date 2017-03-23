

class _SessionInteractionHandler:

    def __init__(self):
        self.handlers = {}

    def interaction(self, expression):
        def decorator(f):
            self.handlers[expression] = f
            return f
        
        return decorator

    def handleInput(self, session, message):
        return "Handling session"
        # handle_function = self.handlers.get(message)
        # if handle_function:
        #     return handle_function(user_id, message)
        # else:
        #     return "Sorry, I don't know what to say."

SessionInteractionHandler = _SessionInteractionHandler()

@SessionInteractionHandler.interaction("start")
def start(user_id, message):
    return """Hey what would you like to do?
    
    Just type \task to get a new task!
    """

@SessionInteractionHandler.interaction("task")
def newTask(worker, message):
    print message
    tasks = TaskService.getAll()
    task = tasks[0]
    newSession = {
        'worker_id': worker['id'],
        'task_id': task['id']
    }
    session = SessionService.insert(newSession)
    return '{}'.format(task['questions'][0]['message'])


