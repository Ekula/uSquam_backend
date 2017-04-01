from session_interaction_handler import SessionInteractionHandler
from idle_interaction_handler import IdleInteractionHandler
from resources.session.service import SessionService
from resources.worker.service import WorkerService
from resources.worker.worker_model import WorkerHandles

class _InteractionRedirector:

    def populateWorker(self, user_id):
        worker = WorkerService.findWhere(username__telegram=str(user_id)).first()
        if worker:
            return worker
        
        handles = WorkerHandles()
        handles.telegram = str(user_id)
        worker = WorkerService.insert({'username': handles})
        return worker

    def onInput(self, user_id, message):
        worker = self.populateWorker(user_id)
        active_session = SessionService.findWhere(worker_id=worker['id'], status='ACTIVE').first()

        if active_session:
            return SessionInteractionHandler.handleInput(active_session, message)
        else:
            return IdleInteractionHandler.handleInput(worker, message)

InteractionRedirector = _InteractionRedirector()
