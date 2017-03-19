from requester_model import Requester


class Service:
    def getAll(self):
        return Requester.objects
    
    def get(self, id):
        return Requester.objects.get(id=id)
    
    def insert(self, in_data):
        from app import app

        # Todo: Check if email already exists

        requester = Requester()
        requester.name = in_data['name']
        requester.password = app.bcrypt.generate_password_hash(in_data['password'])
        requester.email = in_data['email']
        requester.save()

        return requester

RequesterService = Service()