from flask import Blueprint
from flask_restful import Api
from task.blueprint import Task
from requester.blueprint import Requester
from data.blueprint import Data, DataItem

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

# TASKS
api.add_resource(Task, '/tasks', '/tasks/<string:id>')

# REQUESTERS
api.add_resource(Requester, '/requesters', '/requesters/<string:id>')

# Data
api.add_resource(Data,      '/requesters/<string:r_id>/data', '/requesters/<string:r_id>/data/<string:id>')
api.add_resource(DataItem,  '/requesters/<string:r_id>/data/<string:d_id>/items/<string:id>')
