from flask_restful import Resource
from pymongo import MongoClient
from backend.resources.db import client
from backend.common.chatbot import Chatbot
import traceback
from bson import ObjectId
from flask import request
from datetime import datetime

def find_chatroom(room):
    db = client["ChatRooms"]
    all_chatrooms = db["all_chatrooms"]
    room_id = str(room)
    chatroom = all_chatrooms.find_one({ "_id" : ObjectId(room_id) })
    return chatroom, room_id

def update_chatroom(room_id, state):
    db = client["ChatRooms"]
    all_chatrooms = db["all_chatrooms"]

    all_chatrooms.update_one({
        '_id': ObjectId(room_id)
    }, {
        '$set': state
    }, upsert=False)

def create_chatroom(state):
    db = client["ChatRooms"]
    all_chatrooms = db["all_chatrooms"]

    all_chatrooms.insert_one(state)

class ChatbotInitialiseAPI(Resource):
    def post(self):
        request_details = request.get_json()
        room, username = request_details["room"], request_details["username"]
        try:
            if room == "unknown":
                return {'error': "Server Error. Room Does Not Exist."}
            
            chatroom, room_id = find_chatroom(room)

            initial_state = {
                    "_id" : ObjectId(room_id), 
                    "fullName": username, 
                    "roomCreated": datetime.utcnow(),
                    "currentMessage": None,
                    "isAnswering": False,
                    "currentQuestion": None,
                    "questionList": None,
                    "questionIndex": None,
                    "correctAnswers": None,
                    "questionSetMapping": {},
                    "mode": None,
                    "incorrectQuestions": None,
                    "hintIndex": None,
                    "solution": None
                    }

            if chatroom:
                update_chatroom(room_id, initial_state)
            else:
                create_chatroom(initial_state)
        except:
            traceback.print_exc()
            return {'error': "Server Error. There was a problem with your request, please try again."}

class ChatbotAPI(Resource):
    def post(self):
        request_details = request.get_json()
        room, state = request_details["room"], request_details["state"]
        try:
            if room == "unknown":
                return {'error': "Server Error. Room Does Not Exist."}
            
            chatroom, room_id = find_chatroom(room)

            if chatroom:
                state["room_id"] = room_id
                response_message = Chatbot.generate_response(state)

                new_state = {
                    "currentMessage": response_message["message"] if "message" in response_message else None,
                    "isAnswering": response_message["isAnswering"] if "isAnswering" in response_message else None,
                    "currentQuestion": response_message["currentQuestion"] if "currentQuestion" in response_message else None,
                    "questionList": response_message["questionList"] if "questionList" in response_message else None,
                    "questionIndex": response_message["questionIndex"] if "questionIndex" in response_message else None,
                    "mode": response_message["mode"] if "mode" in response_message else None,
                    "correctAnswers": response_message["correctAnswers"] if "correctAnswers" in response_message else None,
                    "incorrectQuestions": response_message["incorrectQuestions"] if "incorrectQuestions" in response_message else None,
                    "hintIndex": response_message["hintIndex"] if "hintIndex" in response_message else None,
                    "solution": response_message["solution"] if "solution" in response_message else None
                }

                update_chatroom(room_id, new_state)

                return {'state': response_message }
            else:
                return {'error': "Server Error. There was a problem with your request, please try again."}
        except:
            traceback.print_exc()
            return {'error': "Server Error. There was a problem with your request, please try again."}
