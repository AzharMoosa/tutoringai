from flask import Flask
from flask_restful import Api
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from flask_apispec.extension import FlaskApiSpec
from resources.chatbot_api import ChatbotAPI

app = Flask(__name__)
api = Api(app)

# Setup Swagger UI
app.config.update({
    'APISPEC_SPEC': APISpec(
        title="Chatbot API",
        version="v1",
        plugins=[MarshmallowPlugin()],
        openapi_version="2.0.0"
    ),
    "APISPEC_SWAGGER_URL": "/swagger/",
    "APISPEC_SWAGGER_UI_URL": "/swagger-ui/"
})
docs = FlaskApiSpec(app)

api.add_resource(ChatbotAPI, "/chatbot")
docs.register(ChatbotAPI)


if __name__ == "__main__":
    app.run(debug=True)
