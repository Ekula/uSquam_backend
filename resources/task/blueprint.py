from flask_restful import Resource
from flask import request, jsonify
from service import *


class Task(Resource):
    def get(self, id):
        task = TaskService.get(id)
        if task:
            return jsonify(task)
        else:
            return None, 404


class TaskList(Resource):
    def post(self):
        json_data = request.get_json(force=True)
        task = TaskService.insert(json_data)
        if task:
            return None, 200
        else: 
            return None, 404