from flask import jsonify, request, make_response
from flask_restful import Resource
from backend.resources.db import client
import traceback
from flask_jwt_extended import jwt_required, get_jwt_identity
from bson import ObjectId
import hashlib

def encrypt_password(password):
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

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

            return make_response(jsonify({"email": user["email"], "fullName": user["fullName"], "_id": user_id, "recentTopics": user["recentTopics"]}), 200)

        except Exception:
            traceback.print_exc()
            return {'error': "Server Error! Unable to create a new user, please try again."}, 500
        
    @jwt_required()
    def put(self):
        try:
            user_id = get_jwt_identity()
            db = client["Users"]
            all_users = db.all_users
            user = all_users.find_one({ "_id" : ObjectId(user_id) })

            # Verify User Exists
            if not user:
                return {"error": "User Does Not Exist!"}, 403

            user_details = request.get_json()

            if "email" in user_details:
                user["email"] = user_details["email"]
            
            if "fullName" in user_details:
                user["fullName"] = user_details["fullName"]
            
            if "password" in user_details:
                user["password"] = encrypt_password(user_details["password"])
            
            # Update User
            all_users.update_one({
                '_id': user["_id"]
            }, {
                '$set': {
                    'fullName': user["fullName"],
                    "email": user["email"],
                    "password": user["password"]
                }
            }, upsert=False)

            return make_response(jsonify({"email": user["email"], "fullName": user["fullName"], "_id": user_id}), 200)
        except Exception:
            traceback.print_exc()
            return {'error': "Server Error! Unable to update user, please try again."}, 500