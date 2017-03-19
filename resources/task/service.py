from task_model import Task

class Service:
    def getAll(self):
        return Task.objects
    
    def get(self, id):
        return Task.objects.get(id=id)
    
    def insert(self, in_task):
        task = Task()
        task.name = in_task['name']
        task.save()
        return True

TaskService = Service()