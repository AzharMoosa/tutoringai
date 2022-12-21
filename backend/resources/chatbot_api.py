from flask_restful import Resource
from flask_apispec.views import MethodResource
from flask_apispec import marshal_with, doc, use_kwargs
from marshmallow import Schema, fields
from pymongo import MongoClient
from backend.resources.db import client
from backend.common.chatbot import Chatbot
import traceback

class ChatbotResponseSchema(Schema):
    output_text = fields.Str(default="I don't understand the question. Please try again.")

class ChatbotRequestSchema(Schema):
    input_text = fields.String(required=True, description="Input Text")

class ChatbotAPI(MethodResource, Resource):
    @doc(description="Generates response from chatbot based on the input text")
    @use_kwargs(ChatbotRequestSchema, location=("json"))
    @marshal_with(ChatbotResponseSchema)
    def post(self, input_text):
        try:
            output_text = Chatbot.generate_response(input_text)
            return { 'output_text': output_text }
        except Exception:
            traceback.print_exc()
            return { 'error': "Server Error. There was a problem with your request, please try again." }