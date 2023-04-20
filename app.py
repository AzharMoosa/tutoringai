from flask import Flask, render_template
from flask_restful import Api
from flask_cors import CORS, cross_origin
from backend.resources.chatbot_api import ChatbotAPI
from backend.resources.chatroom_api import ChatRoomAPI
from backend.resources.auth_api import LoginAPI, RegisterAPI
from backend.resources.user_api import UserAPI
from flask_socketio import SocketIO, join_room, leave_room, send, emit
from backend.common.chatbot import Chatbot
from flask_jwt_extended import JWTManager
import os
from bson import ObjectId
from datetime import datetime

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
    if room == "unknown":
        return
    join_room(room)
    # Create New Room In Database (If Not Exist)
    try:
        db = client["ChatRooms"]
        all_chatrooms = db["all_chatrooms"]

        room_id = str(data["room"])

        chatroom = all_chatrooms.find_one({ "_id" : ObjectId(room_id) })

        if not chatroom:
            print(f"{username} has joined the {room}!")
            all_chatrooms.insert_one({ 
                "_id" : ObjectId(room_id), 
                "fullName": data["username"], 
                "roomCreated": datetime.utcnow(),
                "currentMessage": None,
                "isAnswering": False,
                "currentQuestion": None,
                "questionList": None,
                "questionIndex": None,
                "questionSetMapping": {}
            })
            emit("joined", {"message": f"{username} has joined room"}, to=room)
    except:
        pass

@socketio.on('leave')
def on_leave(data):
    username, room = data["username"], data["room"]
    if room == "unknown":
        return
    leave_room(room)
    # Delete Room In Database (If Exist)
    db = client["ChatRooms"]
    all_chatrooms = db["all_chatrooms"]

    room_id = str(data["room"])

    chatroom = all_chatrooms.find_one({ "_id" : ObjectId(room_id) })

    if chatroom:
        print(f"{username} has left the {room}!")
        all_chatrooms.delete_one({ "_id" : ObjectId(room_id)})
        emit("left", {"message": f"{username} has left room"}, to=room)
    else:
        print(f"Unable to leave {room} as it does not exist!")

@socketio.on('message')
def on_message(data):
    username, state, room = data["username"], data["state"], data["room"]
    if room == "unknown":
        return
    print(f"{username} sent a message to room: {room}!")
    # Update State In Database (If Room Exists)
    db = client["ChatRooms"]
    all_chatrooms = db["all_chatrooms"]

    room_id = str(data["room"])

    chatroom = all_chatrooms.find_one({ "_id" : ObjectId(room_id) })

    if chatroom:
        state["room_id"] = room_id
        response_message = Chatbot.generate_response(state)
        all_chatrooms.update_one({
            '_id': ObjectId(room_id)
        }, {
            '$set': {
                "currentMessage": response_message["message"] if "message" in response_message else None,
                "isAnswering": response_message["isAnswering"] if "isAnswering" in response_message else None,
                "currentQuestion": response_message["currentQuestion"] if "currentQuestion" in response_message else None,
                "questionList": response_message["questionList"] if "questionList" in response_message else None,
                "questionIndex": response_message["questionIndex"] if "questionIndex" in response_message else None,
            }
        }, upsert=False)

        emit("received_message", { "state": response_message }, to=room)
    else:
        print(f"Cannot send message to {room} as it does not exist!")


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
@cross_origin()
def serve(path):
    return render_template("index.html")


api.add_resource(LoginAPI, "/api/auth/login")
api.add_resource(RegisterAPI, "/api/auth/register")
api.add_resource(UserAPI, "/api/users")
api.add_resource(ChatbotAPI, "/api/chatbot")
api.add_resource(ChatRoomAPI, "/api/chatroom")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
    socketio.run(app)
