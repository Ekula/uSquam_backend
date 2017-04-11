from resources.session.service import SessionService
from resources.task.service import TaskService
from resources.data.service import DataService
from resources.worker.service import WorkerService
from resources.session.session_model import Session
from intent import IntentParser
from src.helper_functions import *
import random
import logging


class _IdleSessionHandler:
    def __init__(self):
        self.handlers = {}

    def interaction(self, intent):
        def decorator(f):
            self.handlers[intent] = f
            return f
        
        return decorator

    def handleInput(self, worker, message):
        intent = IntentParser.parse(message, self.handlers.keys())
        if not intent:
            return "Sorry, I don't know what to say."
        
        handle_function = self.handlers.get(intent['intent_type'])

        if handle_function:
            return handle_function(worker, message, intent)
        else:
            return "Sorry, I don't know what to say."

IdleSessionHandler = _IdleSessionHandler()

@IdleSessionHandler.interaction("Number")
def selectTask(session, message, intent):

    if not 'id' in session or not session['type'] == 'IDLE': 
        return 'It seems like you havent listed the tasks first. \
 To select a tasks write "tasks". '

    index = int(intent['NumberKeyword']) - 1
    tasks = TaskService.getAll()

    task = None
    if index < len(tasks):
        task = tasks[index]
    else:
        return "Please choose a task from the list by indicating it's number. Say e.g. '1'"
    
    worker = WorkerService.get(session['worker_id'])

    session.status = "DONE"
    SessionService.update(session)

    new_session = createTaskSessionIntance(worker, task)

    return createTaskInstance(task, new_session)