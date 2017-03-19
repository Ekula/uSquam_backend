from data_model import Data


class Service:
    def getAll(self):
        return Data.objects
    
    def get(self, id):
        return Data.objects.get(id=id)
    
    def insert(self, in_data):
        data = Data()
        var_names = dir(data)
        for key in in_data:
            if key in var_names:
                data[key] = in_data[key]
        data.save()
        return data

    def findWhere(self, **kwargs):
        return Data.objects(**kwargs)

DataService = Service()