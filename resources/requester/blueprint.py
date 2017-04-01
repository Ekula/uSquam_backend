from flask_restful import Resource
from flask import request, jsonify
from service import RequesterService

class Requester(Resource):
    def get(self, id):
        requester = RequesterService.get(id)
        if requester:
            return jsonify(requester)
        else:
            return None, 404

    def get(self):
        return jsonify(RequesterService.getAll())

    def post(self):
        json_data = request.get_json(force=True)
        requester = RequesterService.insert(json_data)
        return jsonify(requester)
