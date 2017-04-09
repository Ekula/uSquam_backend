from task_model import Task, Question

class Service:
    def getAll(self):
        return Task.objects

    def get(self, id):
        return Task.objects.get(id=id)
    
    def generate_reviewtask(self, session, task):
        reviewtask = ReviewTask(session, task)
        reviewtask.answers = session.answers
        
        for item in task['questions']:
            question = Question()
            if 'question_data_idx' in item:
                question.question_data_idx = item['question_data_idx']
            question.message = item['message']
            if 'expected_type' in item:
                question.expected_type = item['expected_type']
            if 'suggestions' in item:
                question.suggestions = item['suggestions']
            reviewtask.questions.append(question)
            
        reviewtask.save()
        return reviewtask
    
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

TaskService = Service()