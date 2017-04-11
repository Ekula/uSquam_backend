from resources.task.service import TaskService
from resources.session.service import SessionService
from resources.data.service import DataService
from resources.session.session_model import Answer
from intent import IntentParser
from resources.requester.service import RequesterService
from resources.worker.service import WorkerService
from src.helper_functions import *

class _SessionInteractionHandler:
    def __init__(self):
        self.handlers = {}

    def interaction(self, intent):
        def decorator(f):
            self.handlers[intent] = f
            return f
        
        return decorator

    def handleInput(self, session, message):
        intent = IntentParser.parse(message, self.handlers.keys())
        handle_function = self.handlers.get(intent['intent_type'])
        if handle_function:
            return handle_function(session, message)

SessionInteractionHandler = _SessionInteractionHandler()

def reviewAnswer(reviewed_session, message):
    print 'newReviewTask'
    result = {}

    print reviewed_session['task_id']
    task = TaskService.getReviewTask(reviewed_session['task_id'])
    session = SessionService.get(task['original_session'])
    original_task = TaskService.get(session['task_id'])
    state = reviewed_session['state']

    answer = Answer()
    answer.message = message
    reviewed_session.answers.append(answer)

    original_answer = session.answers[state]
    review = "Thanks for resubmitting the given answer!"
    if message == 'submit' or message == 'Submit':
        original_answer.validated_answer = session.answers[state].message
    else:
        original_answer.validated_answer = message

    if state + 1 < len(task['questions']):
        state += 1

        question = task['questions'][state]
        original_answer = session['answers'][state]['message']
        data_collection = DataService.get(original_task.data_collection_id)
        task_data = data_collection.task_data.filter(_id=task.task_data_id).first()

        if 'question_data_idx' in task['questions'][0]:
            question_data = task_data.question_data[question['question_data_idx']].content
            review = '{}\n  {}\n {}\n {}'.format(question['message'], question_data, 'Given answer:', original_answer)
        else:
            review = '{}\n {}\n {}'.format(question['message'], 'Given answer:' , original_answer)

        reviewed_session.state = state
        
    else:
        # Give reward to user
        requester = RequesterService.get(original_task['requester_id'])
        worker = WorkerService.get(session['worker_id'])

        reward = task['reward']
        requester['credits'] -= reward
        worker['credits'] += reward

        requester.save()
        worker.save()

        session.validated = True
        reviewed_session.status = "DONE" 
        
    SessionService.update(reviewed_session)
    SessionService.update(session)

    result['answer'] = review
    return result

@SessionInteractionHandler.interaction("Answer")
def newTask(session, message):
    print 'newTask'
    if session.type == 'REVIEW':
        return reviewAnswer(session, message)

    task = TaskService.get(session['task_id'])
    state = session['state']

    answer = Answer()
    answer.message = message
    session.answers.append(answer)

    result = {}

    if state + 1 < len(task['questions']):
        # Prepare a new question for the worker
        state += 1
        session.state = state

        result = formatQuestion(task, session)

    else:
        # Give reward to user
        requester = RequesterService.get(task['requester_id'])
        worker = WorkerService.get(session['worker_id'])

        reward = task['reward']
        requester['credits'] -= reward
        worker['credits'] += reward

        requester.save()
        worker.save()

        answer = 'Thanks! You earned {} credits (Total: {}). Do you have any feedback or comments?'.format(reward, worker['credits'])
        result['answer'] = answer
        session.status = "DONE" # Todo: FEEDBACK status?
    
    SessionService.update(session)
    return result

@SessionInteractionHandler.interaction("CancelTask")
def cancelTask(session, message):
    task = TaskService.get(session['task_id'])
    state = session['state']

    session.status = "STOPPED"

    SessionService.update(session)

    return {'answer': "Okay we stopped your task, thank you for trying!"}
