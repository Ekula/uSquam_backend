from flask_restful import Resource
from flask import request, jsonify
from service import Data

class Task(Resource):
    def get(self, id):
        task = Data.get(id)
        if task:
            return jsonify(task)
        else:
            return None, 404

class DataList(Resource):
    def post(self):
        if Data.insert(request.get_json()):
            return None, 200
        else: 
            return None, 404