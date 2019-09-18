from flask import request, jsonify
from flask_restful import Resource
from oeda.databases import db
import traceback

class TargetController(Resource):

    @staticmethod
    def get(target_id):
        target = db().get_target(target_id)
        try:
            return target
        except:
            return {"error": "not found"}, 404

    @staticmethod
    def post(target_id):
        try:
            target_system = request.get_json()
            # check if given name is unique
            ids, targets = db().get_targets()

            for target in targets:
                if target['name'] == target_system['name']:
                    return {"message": "Duplicate target system names"}, 409

            target_system["status"] = "READY"
            db().save_target(target_system)
            resp = jsonify(target_system)
            resp.status_code = 200
            return resp
        except Exception as e:
            print(e)
            tb = traceback.format_exc()
            print(tb)
            return {"error": e.message}, 404

    @staticmethod
    def put(target_id):
        try:
            if target_id is None:
                return {"message": "target_id should not be null"}, 404
            content = request.get_json()
            status = content["status"]
            db().update_target_system(target_system_id=target_id, field="status", value=status)
            resp = jsonify({"message": "Target system status is updated"})
            resp.status_code = 200
            return resp
        except Exception as e:
            tb = traceback.format_exc()
            print(tb)
            return {"message": e.message}, 404


class TargetsListController(Resource):

    @staticmethod
    def get():
        ids, targets = db().get_targets()
        new_targets = targets
        i = 0
        for _ in targets:
            new_targets[i]["id"] = ids[i]
            i += 1
        new_targets = sorted(new_targets, key=lambda x: x["name"])
        return new_targets

class TargetDeleteController(Resource):

    @staticmethod
    def get(target_id):
        target = db().delete_target(target_id)
        try:
            return target
        except:
            return {"error": "not found"}, 404