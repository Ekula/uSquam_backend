

class MongoDBService:

    def __init__(self, DocumentType):
        self.Document = DocumentType

    def get(self, id):
        return self.Document.objects.get(id=id)

    def getAll(self):
        return self.Document.objects

    def find(self, query):
        pass

    def insert(self, data):
        instance = self.Document()
        for key, value in data.iteritems():
            setattr(instance, key, value)
        
        instance.save()