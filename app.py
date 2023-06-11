from flask import Flask, render_template
from flask_restful import Api
from flask_cors import CORS, cross_origin
from backend.resources.chatbot_api import ChatbotAPI, ChatbotInitialiseAPI
from backend.resources.chatroom_api import ChatRoomAPI
from backend.resources.auth_api import LoginAPI, RegisterAPI
from backend.resources.user_api import UserAPI
from flask_jwt_extended import JWTManager
import os

app = Flask(__name__, static_folder='frontend/build/static',
            template_folder='frontend/build')
app.config["JWT_SECRET_KEY"] = "secret-key"

jwt = JWTManager(app)

CORS(app)
api = Api(app)

# Setup DB
try:
    from backend.resources.db import client
    print("Connected to MongoDB")
except Exception:
    print("Failed to connect to DB")
    exit()

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
@cross_origin()
def serve(path):
    return render_template("index.html")


api.add_resource(LoginAPI, "/api/auth/login")
api.add_resource(RegisterAPI, "/api/auth/register")
api.add_resource(UserAPI, "/api/users")
api.add_resource(ChatbotAPI, "/api/chatbot")
api.add_resource(ChatbotInitialiseAPI, "/api/chatbot/initialise")
api.add_resource(ChatRoomAPI, "/api/chatroom")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
