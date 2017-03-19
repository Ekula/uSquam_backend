from data_model import Data

class Service:
    def getAll(self):
        return Data.objects
    
    def get(self, id):
        return Data.objects.get(id=id)
    
    def insert(self, in_data):
        data = Data()
        data.name = in_data['name']
        data.save()
        return True

TaskService = Service()