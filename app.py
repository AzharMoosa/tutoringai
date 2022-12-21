from flask import Flask, render_template
from flask_restful import Api
from flask_cors import CORS, cross_origin
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from flask_apispec.extension import FlaskApiSpec
from backend.resources.chatbot_api import ChatbotAPI
from backend.resources.chatroom_api import ChatRoomAPI
from flask_socketio import SocketIO, join_room, leave_room, send, emit
from backend.common.chatbot import Chatbot

app = Flask(__name__, static_folder='frontend/build/static',
            template_folder='frontend/build')
CORS(app)
api = Api(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# Setup DB
try:
    from backend.resources.db import client
    print("Connected to MongoDB")
except Exception:
    print("Failed to connect to DB")
    exit()

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

@socketio.on('join')
def on_join(data):
    username, room = data["username"], data["room"]
    join_room(room)
    print(f"{username} has joined the {room}!")
    emit("joined", { "message": f"{username} has joined room"}, to=room)


@socketio.on('leave')
def on_leave(data):
    username, room = data["username"], data["room"]
    leave_room(room)
    print(f"{username} has left the {room}!")
    emit("left", { "message": f"{username} has left room"}, to=room)

@socketio.on('message')
def on_message(data):
    username, message, room = data["username"], data["message"], data["room"]
    print(f"{username} sent: {message} to room: {room}!")
    emit("recieved_message", { "message": Chatbot.generate_response(message) }, to=room)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
@cross_origin()
def serve(path):
    return render_template("index.html")


api.add_resource(ChatbotAPI, "/api/chatbot")
docs.register(ChatbotAPI)
api.add_resource(ChatRoomAPI, "/api/chatroom")
docs.register(ChatRoomAPI)

if __name__ == "__main__":
    app.run(debug=True)
    socketio.run(app)
