from data_model import Data, DataEntry


class Service:
    def getAll(self):
        return Data.objects
    
    def get(self, id):
        return Data.objects.get(id=id)
    
    def insert(self, in_data):
        data = Data()

        print in_data
        data.name = in_data['name']
        data.requester_id = in_data['requester_id']

        for item in in_data['items']:
            entry = DataEntry()
            entry['content'] = item['content']
            data['items'].append(entry)


        # var_names = dir(data)
        # for key in in_data:
        #     if key in var_names:
        #         data[key] = in_data[key]
        data.save()
        return data

    def findWhere(self, **kwargs):
        return Data.objects(**kwargs)

DataService = Service()