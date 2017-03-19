from flask_restful import Resource
from flask import request, jsonify
from service import DataService

class Data(Resource):
    def get(self, r_id, id):
        data = DataService.get(id)
        return jsonify(data)

    def get(self, r_id):
        data = DataService.findWhere(requester_id=r_id)
        return jsonify(data)

    def post(self, r_id):
        json_data = request.get_json(force=True)
        json_data['requester_id'] = r_id
        data = DataService.insert(json_data)
        return jsonify(data)

    # Todo: Patch/put to insert/remove data entries
