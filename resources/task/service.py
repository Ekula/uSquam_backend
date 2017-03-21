from task_model import *

class Service:
    def getAll(self):
        return Task.objects

    def get(self, id):
        return Task.objects.get(id=id)
    
    def insert(self, in_task):
        task = Task()

        task.name = in_task['name']
        task.requester_id = in_task['requester_id']
        task.time_indication = in_task['time_indication']
        task.reward = in_task['reward']
        task.active = in_task['active']

        for item in in_task['questions']:
            question = Question()
            question.data_id = item['data_id']
            question.message = item['message']
            question.expected_type = item['expected_type']
            question.suggestions = item['suggestions']
            task.questions.append(question)
        task.save()
        return task

TaskService = Service()