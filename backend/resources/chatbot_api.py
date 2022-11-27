from flask_restful import Resource
from flask_apispec.views import MethodResource
from flask_apispec import marshal_with, doc, use_kwargs
from marshmallow import Schema, fields


class ChatbotResponseSchema(Schema):
    message = fields.Str(default="Success")


class ChatbotRequestSchema(Schema):
    test = fields.String(required=True, description="Test Description")


class ChatbotAPI(MethodResource, Resource):
    @doc(description="")
    @marshal_with(ChatbotResponseSchema)
    def get(self):
        """

        """
        return {'message': 'TODO'}

    @doc(description="")
    @use_kwargs(ChatbotRequestSchema, location=("json"))
    @marshal_with(ChatbotResponseSchema)
    def post(self):
        """

        """
        return {'message': 'TODO'}

    @doc(description="")
    @marshal_with(ChatbotResponseSchema)
    def delete(self):
        """

        """
        return {'message': 'TODO'}
