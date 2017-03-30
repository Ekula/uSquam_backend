from flask_restful import Resource
from flask import request, jsonify
from service import *


class Task(Resource):

    def get(self, id=None):
        """
        If no ID is specified, return all tasks
        :param id:
        :return:
        """
        if id is None:
            task = TaskService.getAll()
        else:
            task = TaskService.get(id)
        if task:
            return jsonify(task)
        else:
            return None, 404

    def post(self):
        json_data = request.get_json(force=True)
        task = TaskService.insert(json_data)
        if task:
            return None, 200
        else:
            return None, 404
