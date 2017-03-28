from data_model import Data, DataItem


class Service:
    def get(self, r_id, id=None):
        if id is None:
            return Data.objects
        else:
            return Data.objects.get(id=id)
    
    def insert(self, in_data):
        data = Data()

        print in_data
        data.name = in_data['name']
        data.requester_id = in_data['requester_id']

        for item in in_data['items']:
            entry = DataItem()
            entry['content'] = item['content']
            data['items'].append(entry)

        data.save()
        return data

    def findWhere(self, **kwargs):
        return Data.objects(**kwargs)

    def update(self, in_data):
        data = Data.objects.get(id=in_data['id'])
        data.name = in_data['name']
        data.requester_id = in_data['requester_id']

        for item in in_data['items']:
            entry = DataItem()
            entry['content'] = item['content']
            data['items'].append(entry)

        data.save()
        return data

DataService = Service()