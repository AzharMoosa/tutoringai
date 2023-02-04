from flask import Flask, render_template
from flask_restful import Api
from flask_cors import CORS, cross_origin
from backend.resources.chatbot_api import ChatbotAPI
from backend.resources.chatroom_api import ChatRoomAPI
from backend.resources.auth_api import LoginAPI, RegisterAPI
from flask_socketio import SocketIO, join_room, leave_room, send, emit
from backend.common.chatbot import Chatbot
from flask_jwt_extended import JWTManager

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
    username, message, room = data["username"], data["message"], data["room"]
    print(f"{username} sent: {message} to room: {room}!")
    emit("recieved_message", {
         "message": Chatbot.generate_response(message)}, to=room)


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
    app.run(debug=True)
    socketio.run(app)
