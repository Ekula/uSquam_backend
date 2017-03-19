from flask import Blueprint
from flask_restful import Api
from task.blueprint import Task, TaskList
from requester.blueprint import Requester
from data.blueprint import Data

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

# TASKS
api.add_resource(Task, '/tasks/<string:id>')
api.add_resource(TaskList, '/tasks')
# api.add_resource(Task, '/requesters/<string:r_id>/tasks/<string:id>')


# REQUESTERS
api.add_resource(Requester, '/requesters', '/requesters/<string:id>')


# Data
api.add_resource(Data, '/requesters/<string:r_id>/data', '/requesters/<string:r_id>/data/<string:id>')