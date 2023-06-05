from flask import jsonify, request, make_response
from flask_restful import Resource
from pymongo import MongoClient
from backend.resources.db import client
from backend.common.chatbot import Chatbot
import datetime
import traceback
from flask_jwt_extended import create_access_token
import hashlib


def encrypt_password(password):
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


class LoginAPI(Resource):
    def post(self):
        try:
            user_details = request.get_json()
            db = client["Users"]
            all_users = db.all_users

            # Get User Details
            email = user_details["email"]
            password = user_details["password"]

            user = all_users.find_one({"email": email})

            # Verify User Exists
            if not user:
                return {'error': "User does not exist!"}, 403

            # Generate JWT Token
            token = create_access_token(identity=str(user["_id"]), expires_delta=datetime.timedelta(days=30))

            encrypted_password = encrypt_password(password)

            if encrypted_password != user["password"]:
                return {'error': "Invalid email or password!"}, 403

            return make_response(jsonify({"email": user["email"], "fullName": user["fullName"], "token": token, "_id": str(user["_id"]), "recentTopics": user["recentTopics"]}), 200)
        except Exception:
            traceback.print_exc()
            return {'error': "Server Error! Unable to create a new user, please try again."}, 500


class RegisterAPI(Resource):
    def post(self):
        try:
            user_details = request.get_json()
            db = client["Users"]
            all_users = db.all_users

            # Get User Details
            email = user_details["email"]
            full_name = user_details["fullName"]
            password = user_details["password"]

            user = all_users.find_one({"email": email})

            # Verify User Does Not Exists
            if user:
                return {"error": "User already exist!"}, 403

            # Create User
            current_date = datetime.datetime.today()
            hashed_password = encrypt_password(password)
            created_user = all_users.insert_one(
                {"createdDate": current_date, "email": email, "fullName": full_name, "password": hashed_password, "recentTopics": []})

            # Generate JWT Token
            token = create_access_token(identity=str(created_user.inserted_id), expires_delta=datetime.timedelta(days=30))

            return make_response(jsonify({"email": email, "fullName": full_name, "token": token, "_id": str(created_user.inserted_id), "recentTopics": []}), 200)
        except Exception:
            traceback.print_exc()
            return {'error': "Server Error! Unable to create a new user, please try again."}, 500
