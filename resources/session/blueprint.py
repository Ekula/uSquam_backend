from flask_restful import Resource
from flask import request, jsonify
from service import *


class Session(Resource):

    def get(self, t_id=None, id=None):
        """
        If no ID is specified, return all tasks
        :param id:
        :return:
        """
        if id is None:
            task = SessionService.findWhere(task_id=t_id)
        else:
            task = SessionService.get(id)
        if task:
            return jsonify(task)
        else:
            return None, 404
