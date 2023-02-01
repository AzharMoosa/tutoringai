from flask_restful import Resource
from flask_apispec.views import MethodResource
from flask_apispec import marshal_with, doc, use_kwargs
from marshmallow import Schema, fields
from pymongo import MongoClient
from backend.resources.db import client
from backend.common.chatbot import Chatbot
import datetime
import traceback
from flask_jwt_extended import create_access_token
import hashlib

class LoginResponseSchema(Schema):
    current_date = fields.Date()
    email = fields.Str()
    fullName = fields.Str()
    token = fields.Str()
    _id = fields.Str()


class LoginRequestSchema(Schema):
    email = fields.String(required=True, description="User's Email")
    password = fields.String(required=True, description="User's Password")


class RegisterResponseSchema(Schema):
    current_date = fields.Date()
    email = fields.Str()
    fullName = fields.Str()
    token = fields.Str()
    _id = fields.Str()


class RegisterRequestSchema(Schema):
    full_name = fields.String(required=True, description="User's Full Name")
    email = fields.String(required=True, description="User's Email Address")
    password = fields.String(required=True, description="User's Password")

class LoginAPI(MethodResource, Resource):
    @doc(description="TODO")
    @use_kwargs(LoginRequestSchema, location=("json"))
    @marshal_with(LoginResponseSchema)
    def post(self, email, password):
        try:
            db = client["Users"]
            all_users = db.all_users

            user = all_users.find_one({}, { "email": email })

            # Verify User Exists
            if not user:
                return { 'error' : "Invalid email or password!" }, 403
            
            # Generate JWT Token
            token = create_access_token(identity=user["_id"])

            encrypted_password = hashlib.sha256(password.encode("utf-8")).hexdigest()

            if encrypted_password != password:
                return { 'error' : "Invalid email or password!" }, 403
            
            return { "createdDate": user["createdDate"], "email": email, "fullName": user["fullName"], "token": token, "_id": user["_id"] }, 200
        except Exception:
            traceback.print_exc()
            return { 'error': "Server Error! Unable to create a new chatroom, please try again." }, 500
        
class RegisterAPI(MethodResource, Resource):
    @doc(description="Registers a new user into the database.")
    @use_kwargs(RegisterRequestSchema, location=("json"))
    @marshal_with(RegisterResponseSchema)
    def post(self, full_name, email, password):
        try:
            db = client["Users"]
            all_users = db.all_users

            user = all_users.find_one({}, { "email": email })

            # Verify User Does Not Exists
            if user:
                return { 'error' : "User already exist!" }, 403

            # Create User
            current_date = datetime.datetime.today()
            password = hashlib.sha256(password.encode("utf-8")).hexdigest()
            created_user = all_users.insert_one({ "createdDate": current_date, "email": email, "fullName": full_name, "password": password })

            # Generate JWT Token
            token = create_access_token(identity=created_user.inserted_id)

            return { "createdDate": current_date, "email": email, "fullName": full_name, "token": token, "_id": created_user.inserted_id }, 200
        except Exception:
            traceback.print_exc()
            return { 'error': "Server Error! Unable to create a new chatroom, please try again." }, 500