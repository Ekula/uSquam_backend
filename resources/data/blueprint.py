from flask_restful import Resource
from flask import request, jsonify
from service import DataService

class Data(Resource):
    def get(self, r_id, id=None):
        if id is None:
            data = DataService.findWhere(requester_id=r_id)
            return jsonify(data)

        data = DataService.get(r_id, id)
        print data.requester_id, r_id
        if str(data.requester_id) == r_id:
            return jsonify(data)
        return 403

    def post(self, r_id):
        json_data = request.get_json(force=True)
        json_data['requester_id'] = r_id
        data = DataService.insert(json_data)
        return jsonify(data)

    def put(self, r_id):
        json_data = request.get_json(force=True)
        if json_data['id'] is not None:
            return jsonify(DataService.update(json_data))
        return 500


class DataItem(Resource):
    def get(self, r_id, d_id, id):
        data = DataService.findWhere(requester_id=r_id, id=d_id)
        for i in range(len(data)):
            for j in range(len(data[i].task_data)):
                if str(data[i].task_data[j]._id) == id:
                    return jsonify(data[i].task_data[j])
        return 404


