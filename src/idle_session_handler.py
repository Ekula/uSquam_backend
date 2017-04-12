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
        self.actions = {}

    def interaction(self, intent):
        def decorator(f):
            self.handlers[intent] = f
            return f
        
        return decorator

    def action(self, action):
        def decorator(f):
            self.actions[action] = f
            return f
        
        return decorator

    def handleInput(self, session, message):
        print session['task_id']
        task = TaskService.findIdleTaskWhere(id=session['task_id']).first()

        intents = []
        state = task.states[session.state]
        for action in state.actions:
            if action.intent not in intents:
                intents.append(action.intent)

        # Check if message is a location (so uuuugly)
        intent = None
        if type(message) is dict and 'latitude' in message:
            intent = {'intent_type': 'Location'} # listNearbyTasks(session, message)
        else:
            intent = IntentParser.parse(message, intents)
        if not intent:
            return {'answer': "Sorry, I don't know what to say."}
        
        action = state.actions.filter(intent=intent['intent_type']).first()
        handle_function = self.actions.get(action.action)

        reply = ""
        if handle_function:
            reply =  handle_function(session, message, intent)
            if session.status == "ACTIVE":
                if session.state + 1 < len(task.states):
                    session.state = session.state + 1
                else:
                    session.status = "DONE"
                SessionService.update(session)
        else:
            reply = {'answer': "Sorry, I don't know what to say."}

        return reply

IdleSessionHandler = _IdleSessionHandler()

@IdleSessionHandler.action("SelectTask")
def selectTask(session, message, intent):
    logging.info("Select task")
    index = int(intent['NumberKeyword']) - 1
    tasks = TaskService.getAll()

    task = None
    if index < len(tasks):
        task = tasks[index]
    else:
        return {'answer': "Please choose a task from the list by indicating it's number. Say e.g. '1'"}
    
    worker = WorkerService.get(session['worker_id'])

    # session.status = "DONE"
    # SessionService.update(session)

    new_session = createTaskSessionIntance(worker, task)

    return formatQuestion(task, new_session)

@IdleSessionHandler.action("CancelTask")
def cancelTask(session, message, intent):
    logging.info("Cancel task")

    session.status = "ON_HOLD"
    SessionService.update(session)
    # Todo: Delete session? Not useful anymore

    return {'answer': "Alright, putting this session on hold! If you need help, just send 'I need help'"}

@IdleSessionHandler.action("ListSituationalTasks")
def listNearbyTasks(session, coords, intent):
    logging.info("Listing nearby tasks")
    task = TaskService.findIdleTaskWhere(id=session['task_id']).first()

    # Todo: Update worker properties, something like
    # worker.properties.coordinates = [coords.longitude, coords.longitude]
    # worker.properties.coordinates_updated = datetime.datetime.now

    # Todo: Find nearby tasks
    # ...


    # Todo: If no tasks were found
    # session.status = "STOPPED"
    # SessionService.update(session)

    return {'answer': 'These are the tasks near you. \n\n1. blabla\n\n{}'.format(task.states[session.state].question),
        'suggestions': ['1', '2', '3', '4', '5', 'Cancel']
    }

@IdleSessionHandler.action("SelectSituationalTask")
def selectSituationalTask(session, message, intent):
    logging.info("Starting the chosen situational task")

    session.status = "STOPPED"
    SessionService.update(session)

    return {'answer': 'I could not select that task, not sure if this function is implemented yet'}