from task_model import *

class Service:
    def getAll(self):
        return Task.objects
    
    def get(self, id):
        return Task.objects.get(id=id)
    
    def insert(self, in_task):
        task = Task()
        var_names = dir(task)
        for key in in_task:
            if key in var_names:
                task[key] = in_task[key]
        task.save()
        return task

TaskService = Service()