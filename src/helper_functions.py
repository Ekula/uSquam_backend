from resources.session.service import SessionService
from resources.task.service import TaskService
from resources.data.service import DataService
from resources.worker.service import WorkerService
from resources.session.session_model import Session
import random

def formatQuestion(task, session):
    """
    Formats a question from a task to a worker, including a question_data and suggestions if they are defined.
    The state of the sessions should be adjusted before calling this functionn, since the question
    that is asked depends on the state
    :param task: The task that is being executed
    :param session: The current session of the worker
    :return: A dictionary containing an answer and optionally an array of answer suggestions
    """
    state = session['state']
    question = task['questions'][state]['message']
    result = {}

    # Find question data content
    data_collection = DataService.get(task['data_collection_id'])
    task_data = None
    for item in data_collection['task_data']:
        if str(item['_id']) == str(session['task_data_id']):
            task_data = item
            break

    # There could be no data item specified for this question
    if 'question_data_idx' in task['questions'][state]:
        question_data = task_data.question_data[task['questions'][state]['question_data_idx']]
        if question_data.type != 'IMAGE':
            result['markdown'] = True
            answer = '{}\n  *{}*'.format(question, question_data.content)
        else:
            answer = '{}\n  {}'.format(question, question_data.content)

    else:
        answer = '{}'.format(question)

    if state == 0 and task.coordinates is not None:
        result['send_location'] = {'latitude': task['coordinates']['coordinates'][0],
                                   'longitude': task['coordinates']['coordinates'][1]}

    # Check if there suggestions to be used as buttons in the chat application
    if 'suggestions' in task['questions'][state]:
        result['suggestions'] = task['questions'][state].suggestions

    result['answer'] = answer
    return result

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