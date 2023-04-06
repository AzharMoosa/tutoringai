import re
import json
from json import JSONEncoder
import os
from question import Question, QuestionEncoder
from pymongo import MongoClient
from dotenv import load_dotenv
import os
load_dotenv()
client = MongoClient(os.getenv("MONGODB_URI"), serverSelectionTimeoutMS=5000)

__location__ = os.path.realpath(os.path.join(
    os.getcwd(), os.path.dirname(__file__)))


class QuestionEngine:
    pass