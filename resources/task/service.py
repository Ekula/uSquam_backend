from task_model import Task, Question, ReviewTask, IdleTask, Action, State
import traceback

class Service:
    def getAll(self):
        return Task.objects

    def get(self, id):
        return Task.objects.get(id=id)
    
    def generate_reviewtask(self, session, task):
        reviewtask = ReviewTask()
        reviewtask.task_id = task['id']
        reviewtask.task_data_id = session['task_data_id']
        reviewtask.worker_id = session['worker_id']
        reviewtask.original_session = session['id']
        reviewtask.answers = session.answers
        reviewtask.questions = task.questions
        reviewtask.reward = 100.0
            
        reviewtask.save()
        return reviewtask

    def getReviewTask(self, id):
        return ReviewTask.objects.get(id=id)

    def insert(self, in_task):
        task = Task()

        task.name = in_task['name']
        task.requester_id = in_task['requester_id']
        task.time_indication = in_task['time_indication']
        task.reward = in_task['reward']
        task.gpsbased = in_task['gps_based']
        task.data_collection_id = in_task['data_collection_id']
        
        if 'active' in in_task:
            task.active = in_task['active']
              
        for item in in_task['questions']:
            question = Question()
            if 'question_data_idx' in item:
                question.question_data_idx = item['question_data_idx']
            question.message = item['message']
            if 'expected_type' in item:
                question.expected_type = item['expected_type']
            if 'suggestions' in item:
                question.suggestions = item['suggestions']
            task.questions.append(question)
        task.save()
        return task

    def createIdleTask(self, idle_task):

        task = IdleTask()
        task.name = idle_task['name']
        
        state_dict = idle_task['states']
        for in_state in state_dict:
            state = State()
            state.question = in_state['question']

            for in_intent, in_action in in_state['actions'].iteritems():
                action = Action()
                action.intent = in_intent
                action.action = in_action

                state.actions.append(action)
            
            task.states.append(state)

        task.save()
        return task

    def findWhere(self, **kwargs):

        return Task.objects(**kwargs)

    def findIdleTaskWhere(self, **kwargs):

        return IdleTask.objects.get(**kwargs)

TaskService = Service()

### Create some standard IdleTasks
try:
    # Replace before create
    idle_task = TaskService.findIdleTaskWhere(name='SelectTask')
    if idle_task is not None:
        idle_task.delete()

    TaskService.createIdleTask({
        "name": "SelectTask",
        "states": [
            {
                "question": "Please select a task by sending its number.",
                "actions": {
                    "Number": "SelectTask",
                    "CancelTask": "CancelTask"
                }
            }
        ]
    })
except Exception: 
    traceback.print_exc()
    print "Could not create the SelectTask task"

try:
    # Replace before create
    idle_task = TaskService.findIdleTaskWhere(name='SituationalTask')
    if idle_task is not None:
        idle_task.delete()

    TaskService.createIdleTask({
        "name": "SituationalTask",
        "states": [
            {
                "question": "Can you share your location with me?",
                "actions": {
                    "Location": "ListSituationalTasks",
                    "CancelTask": "CancelTask"
                }
            },
            {
                "question": "Please select a task",
                "actions": {
                    "Number": "SelectSituationalTask",
                    "CancelTask": "CancelTask"
                }
            }
        ]
    })
except:
    traceback.print_exc()
    print "Could not create the SelectTask task"
