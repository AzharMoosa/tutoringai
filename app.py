from flask import Flask, render_template
from flask_restful import Api
from flask_cors import CORS, cross_origin
from backend.resources.chatbot_api import ChatbotAPI
from backend.resources.chatroom_api import ChatRoomAPI
from backend.resources.auth_api import LoginAPI, RegisterAPI
from flask_socketio import SocketIO, join_room, leave_room, send, emit
from backend.common.chatbot import Chatbot
from backend.common.question_engine.question_engine import generated_questions
from flask_jwt_extended import JWTManager
import os

app = Flask(__name__, static_folder='frontend/build/static',
            template_folder='frontend/build')
app.config["JWT_SECRET_KEY"] = "secret-key"

jwt = JWTManager(app)

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


@socketio.on('join')
def on_join(data):
    username, room = data["username"], data["room"]
    join_room(room)
    print(f"{username} has joined the {room}!")
    emit("joined", {"message": f"{username} has joined room"}, to=room)


@socketio.on('leave')
def on_leave(data):
    username, room = data["username"], data["room"]
    leave_room(room)
    print(f"{username} has left the {room}!")
    emit("left", {"message": f"{username} has left room"}, to=room)


@socketio.on('message')
def on_message(data):
    username, message_info, room = data["username"], data["messageInfo"], data["room"]
    print(f"{username} sent a message to room: {room}!")
    # message = Chatbot.generate_response(message_info["message"])
    if message_info["isAnswering"]:
        response_message = "Thats correct!" if generated_questions[0][0].is_correct(
            message_info["message"]) else "Sorry that is wrong"
    else:
        response_message = generated_questions[0][0].question
    emit("received_message", {
         "message": response_message}, to=room)


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
@cross_origin()
def serve(path):
    return render_template("index.html")


api.add_resource(LoginAPI, "/api/auth/login")
api.add_resource(RegisterAPI, "/api/auth/register")
api.add_resource(ChatbotAPI, "/api/chatbot")
api.add_resource(ChatRoomAPI, "/api/chatroom")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
    socketio.run(app)
