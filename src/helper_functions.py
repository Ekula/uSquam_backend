from resources.session.service import SessionService
from resources.task.service import TaskService
from resources.data.service import DataService
from resources.worker.service import WorkerService
from resources.session.session_model import Session
import random

def createTaskInstance(task, session):
    question = task['questions'][0]['message']
    # Todo: Create a question format function somewhere (same code in session_interaction_handler)
    # Find question data content
    data_collection = DataService.get(task['data_collection_id'])
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

def createTaskSessionIntance(worker, task):
    data_collection = DataService.get(task['data_collection_id'])

    task_data = random.choice(data_collection['task_data'])
    new_session = {
        'worker_id': worker['id'],
        'task_id': task['id'],
        'task_data_id': task_data['_id'],
        'review': False
    }
    return SessionService.insert(new_session)

def createReviewSessionIntance(worker, task):
    new_session = {
        'worker_id': worker['id'],
        'task_id': task['id'],
        'type': 'REVIEW',
        'review': False
    }
    return SessionService.insert(new_session)


def createIdleSessionInstance(worker, task):
    new_session = {
        'worker_id': worker['id'],
        'task_id': task['id'],
        'task_data_id': None,
        'type': 'IDLE',
        'review': False
    }
    return SessionService.insert(new_session)