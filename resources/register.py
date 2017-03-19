from flask import Blueprint
from flask_restful import Api
from task.blueprint import *

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

# TASKS
api.add_resource(Task, '/tasks/<string:id>')
api.add_resource(TaskList, '/tasks')
