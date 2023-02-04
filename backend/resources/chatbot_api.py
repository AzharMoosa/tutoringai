from flask_restful import Resource
from pymongo import MongoClient
from backend.resources.db import client
from backend.common.chatbot import Chatbot
import traceback


class ChatbotAPI(Resource):
    def post(self, input_text):
        try:
            output_text = Chatbot.generate_response(input_text)
            return {'output_text': output_text}
        except Exception:
            traceback.print_exc()
            return {'error': "Server Error. There was a problem with your request, please try again."}
