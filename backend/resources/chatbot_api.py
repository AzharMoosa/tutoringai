from flask_restful import Resource
from pymongo import MongoClient
from backend.resources.db import client
from backend.common.chatbot import Chatbot
import traceback


class ChatbotAPI(Resource):
    def post(self, input_text):
        try:
            return {'output_text': "TODO"}
        except Exception:
            traceback.print_exc()
            return {'error': "Server Error. There was a problem with your request, please try again."}
