from resources.task.service import TaskService
from resources.session.service import SessionService
from resources.data.service import DataService
from resources.session.session_model import Answer
from intent import IntentParser

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
            return handle_function(session, intent['intent_type'])

SessionInteractionHandler = _SessionInteractionHandler()

@SessionInteractionHandler.interaction("Answer")
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

        question = task['questions'][state]['message']

        # Todo: Create a question format function somewhere (same code in idle_interaction_handler)
        # Find question data content
        data_collection = DataService.get(None, task['data_collection_id'])
        task_data = None
        for item in data_collection['task_data']:
            print item['_id'], session['task_data_id']
            if str(item['_id']) == str(session['task_data_id']):
                task_data = item
                break

        # There could be no data item specified for this question
        if 'question_data_idx' in task['questions'][state]:
            question_data = task_data.question_data[task['questions'][state]['question_data_idx']].content
            answer = '{}\n  {}'.format(question, question_data)
        else:
            answer = '{}'.format(question)
        session.state = state
        
    else:
        answer = "Thank you for completing the task"
        session.status = "DONE"
    
    SessionService.update(session)
    
    return answer


