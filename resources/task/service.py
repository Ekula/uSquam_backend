

class Service:
    TASKS = [
        {
            'questions': [
                {
                    'id': 1,
                    'query': 'Make a selfie with a happy face'
                }
            ]
        }
    ]

    def getAll(self):
        return self.TASKS
    
    def get(self, id):
        tasks = self.getAll()

        if id < len(tasks):
            return tasks[id]
        else:
            return None
    
    def insert(self, task):
        if not task:
            return False
        self.TASKS.append(task)
        return True

TaskService = Service()