from flask import Blueprint
from flask_restful import Api
from task.blueprint import Task, TaskList

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

api.add_resource(Task, '/tasks/<int:id>')
api.add_resource(TaskList, '/tasks')