from flask_restful import Resource
from pymongo import MongoClient
from backend.resources.db import client
from backend.common.chatbot import Chatbot
import datetime
import traceback


class ChatRoomAPI(Resource):
    def post(self, user_id):
        try:
            db = client["ChatRooms"]
            all_chatrooms = db.all_chatrooms
            current_date = datetime.datetime.today()
            created_room = all_chatrooms.insert_one(
                {"date": current_date, "user_id": user_id})
            return {"date": current_date, "user_id": user_id, "_id": created_room.inserted_id}
        except Exception:
            traceback.print_exc()
            return {'error': "Server Error! Unable to create a new chatroom, please try again."}
