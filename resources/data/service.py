from data_model import DataCollection, TaskData, QuestionData


class Service:
    def getAll(self):
        return DataCollection.objects

    def get(self, r_id, id=None):
        if id is None:
            return DataCollection.objects
        else:
            return DataCollection.objects.get(id=id)
    
    def insert(self, in_data):
        data = DataCollection()
        data.name = in_data['name']
        data.requester_id = in_data['requester_id']

        for item in in_data['task_data']:
            entry = TaskData()
            for q_item in item['question_data']:
                q_data = QuestionData()
                q_data.content = q_item['content']
                q_data.type = q_item['type']
                entry.question_data.append(q_data)
            data.task_data.append(entry)

        data.save()
        return data

    def findWhere(self, **kwargs):
        return DataCollection.objects(**kwargs)

    def update(self, in_data):
        data = DataCollection.objects.get(id=in_data['id'])
        data.name = in_data['name']
        data.requester_id = in_data['requester_id']

        for item in in_data['task_data']:
            entry = TaskData()
            for q_item in item['question_data']:
                q_data = QuestionData()
                q_data.content = q_item['content']
                q_data.type = q_item['type']
                entry.question_data.append(q_data)
            data.task_data.append(entry)

        data.save()
        return data

DataService = Service()
