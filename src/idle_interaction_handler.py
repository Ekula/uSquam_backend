# -*- coding: utf-8 -*-

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
        intent = ''
        if message.startswith('http'):
            intent = 'Answer'
        else:
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
*task* - You can send me ‘_Give me a task_’ or something similar for a randomly selected task.

*tasks* - You can send me ‘_Give me tasks_’ or something similar for a list of all available tasks. Then you will be able to select a task yourself.

*review task* - You can send me ‘_I want a review task_’ or something similar to review the answer that have been submitted by someone else.

*nearby task* - You can send me ‘_I want a nearby task_’ or something similar to perform a task that is located within a 3 km range of your current GPS location.

*cancel* - You can send me ‘_I want to cancel my task_’ or something similar to stop the task you are working on.

*help* - If you need any _help_, let me know!
""", 'markdown': True}

@IdleInteractionHandler.interaction("TaskList")
def taskList(worker, message, intent):
    # Only use active, non-situational tasks
    tasks = TaskService.findWhere(active=True, coordinates=None)

    answer = "These are the tasks that are currently available: \
 \n\n{}\n\nWhich task would you like?".format("\n".join(["{}. {}".format(i+1, task.name) for i, task in enumerate(tasks)]))

    task = TaskService.findIdleTaskWhere(name="SelectTask").first()

    session = createIdleSessionInstance(worker, task)

    return {'answer': "\n".join([answer, task.states[0].question]), 'suggestions': ['1', '2', '3', '4', '5', 'Cancel']}

@IdleInteractionHandler.interaction("NewTask")
def newTask(worker, message, intent):
    print 'Received: ', message, ' - Creating new task'
    # Choose random task and random item from data collection
    tasks = TaskService.findWhere(active=True, coordinates=None)
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
        review = '{}\n {}\n {}'.format(question['message'], '**Given answer:**' , answer)

    session = createReviewSessionIntance(worker, reviewtask)

    return {'answer': review}


@IdleInteractionHandler.interaction("SituationalTaskList")
def taskList(worker, message, intent):

    # Todo: Check how long ago location was updated

    task = TaskService.findIdleTaskWhere(name="SelectSituationalTask").first()
    session = createIdleSessionInstance(worker, task)

    return {'answer': task.states[0].question, 'location': True}