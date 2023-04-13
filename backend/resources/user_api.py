from flask import jsonify, make_response
from flask_restful import Resource
from backend.resources.db import client
import traceback
from flask_jwt_extended import jwt_required, get_jwt_identity
from bson import ObjectId

class UserAPI(Resource):
    @jwt_required()
    def get(self):
        try:
            user_id = get_jwt_identity()
            db = client["Users"]
            all_users = db.all_users
            user = all_users.find_one({ "_id" : ObjectId(user_id) })

            # Verify User Exists
            if not user:
                return {"error": "User Does Not Exist!"}, 403

            return make_response(jsonify({"email": user["email"], "fullName": user["fullName"], "_id": user_id}), 200)

        except Exception:
            traceback.print_exc()
            return {'error': "Server Error! Unable to create a new user, please try again."}, 500
