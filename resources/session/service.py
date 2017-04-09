from session_model import Session

class Service:
    def insert(self, in_session):

        session = Session()
        session.task_id = in_session['task_id']
        session.task_data_id = in_session['task_data_id']
        session.worker_id = in_session['worker_id']
        session.review = in_session['review']
        if 'status' in in_session:
            session.status = in_session['status']
        if 'state' in in_session:
            session.state = in_session['state']

        session.save()
        return session

    def update(self, session):
        session.save()
    
    def getAll(self):
        return Session.objects

    def findWhere(self, **kwargs):

        return Session.objects(**kwargs)

SessionService = Service()