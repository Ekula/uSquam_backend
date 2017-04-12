from resources.session.service import SessionService
from resources.task.service import TaskService
from resources.data.service import DataService
from resources.worker.service import WorkerService
from resources.session.session_model import Session
from intent import IntentParser
from src.helper_functions import *
import random
import logging
import datetime
from math import sin, cos, sqrt, atan2, radians


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
            reply = handle_function(session, message, intent)
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

    print coords

    # Update worker properties
    worker = WorkerService.get(session['worker_id'])
    worker.coordinates = [coords['latitude'], coords['longitude']]
    worker.coordinates_updated = datetime.datetime.now

    result = {}
    # Find nearby tasks
    nearby_tasks = selectGPSTasks(coords)

    if len(nearby_tasks) > 0:
        session.cache = {'nearby_tasks': nearby_tasks}
        SessionService.update(session)
        result = {'answer': "These are the tasks near you.  \n\n{}\n\nWhich task would you like?"
            .format("\n".join(["{}. {} ({} km)".format(i+1, dis_task['task'].name, dis_task['distance']) for i, dis_task in enumerate(nearby_tasks)])),
                  'suggestions': ['1', '2', '3', '4', '5', 'Cancel']}
    else:
        session.status = "STOPPED"
        SessionService.update(session)
        result = {'answer': 'Sorry, no nearby tasks were found!'}

    return result


@IdleSessionHandler.action("SelectSituationalTask")
def selectSituationalTask(session, message, intent):
    logging.info("Starting the chosen situational task")
    index = int(intent['NumberKeyword']) - 1
    nearby_tasks = session.cache['nearby_tasks']

    task = None
    if index < len(nearby_tasks):
        task = nearby_tasks[index]['task']
    else:
        return {'answer': "Please choose a task from the list by indicating it's number. Say e.g. '1'"}

    worker = WorkerService.get(session['worker_id'])

    new_session = createTaskSessionIntance(worker, task)

    return formatQuestion(task, new_session)


def selectGPSTasks(worker_coords):
    tasks = TaskService.getAll()
    suitableGPSTasks = []

    for task in tasks:
        task_coords = task.coordinates
        if task_coords is not None:
            task_coords = task_coords['coordinates']
            distance = calculateDistance(task_coords[0], task_coords[1],
                                         worker_coords['latitude'], worker_coords['longitude'])
            if distance <= 3:
                suitableGPSTasks.append({'task': task, 'distance': distance})

    return suitableGPSTasks

def calculateDistance(lat1, lon1, lat2, lon2):
    R = 6373.0

    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c

    return distance