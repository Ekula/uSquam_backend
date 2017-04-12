from worker_model import Worker, WorkerProperties

class Service:

    def get(self, id):
        return Worker.objects.get(id=id)

    def insert(self, in_worker):

        worker = Worker()
        worker.username = in_worker['username']
        worker.properties = WorkerProperties()
        worker.save()

        return worker

    def findWhere(self, **kwargs):

        return Worker.objects(**kwargs)

WorkerService = Service()