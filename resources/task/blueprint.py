from flask_restful import Resource
from flask import request, jsonify
from service import TaskService

class Task(Resource):
    def get(self, id):
        task = TaskService.get(id)
        if task:
            return jsonify(task)
        else:
            return None, 404

class TaskList(Resource):
    def post(self):
        if TaskService.insert(request.get_json()):
            return None, 200
        else: 
            return None, 404