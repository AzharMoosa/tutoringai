from flask import Flask, render_template
from flask_restful import Api
from flask_cors import CORS, cross_origin
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from flask_apispec.extension import FlaskApiSpec
from backend.resources.chatbot_api import ChatbotAPI

app = Flask(__name__, static_folder='frontend/build/static',
            template_folder='frontend/build')
CORS(app)
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


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
@cross_origin()
def serve(path):
    return render_template("index.html")


api.add_resource(ChatbotAPI, "/chatbot")
docs.register(ChatbotAPI)


if __name__ == "__main__":
    app.run(debug=True)
