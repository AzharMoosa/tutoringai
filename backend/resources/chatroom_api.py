from flask_restful import Resource
from flask_apispec.views import MethodResource
from flask_apispec import marshal_with, doc, use_kwargs
from marshmallow import Schema, fields
from pymongo import MongoClient
from backend.resources.db import client
from backend.common.chatbot import Chatbot
import datetime
import traceback

class ChatRoomResponseSchema(Schema):
    date = fields.Date()
    user_id = fields.Str()
    _id = fields.Str()


class ChatRoomRequestSchema(Schema):
    user_id = fields.String(required=True, description="User ID")

class ChatRoomAPI(MethodResource, Resource):
    @doc(description="Create a new chatroom session")
    @use_kwargs(ChatRoomRequestSchema, location=("json"))
    @marshal_with(ChatRoomResponseSchema)
    def post(self, user_id):
        try:
            db = client["ChatRooms"]
            all_chatrooms = db.all_chatrooms
            current_date = datetime.datetime.today()
            created_room = all_chatrooms.insert_one({ "date": current_date, "user_id": user_id })
            return { "date": current_date, "user_id": user_id, "_id": created_room.inserted_id }
        except Exception:
            traceback.print_exc()
            return { 'error': "Server Error! Unable to create a new chatroom, please try again." }