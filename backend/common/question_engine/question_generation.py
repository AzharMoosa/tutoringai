import json
from backend.common.question_engine.question import Question
from backend.resources.db import client
import os

__location__ = os.path.realpath(os.path.join(
    os.getcwd(), os.path.dirname(__file__)))

def retrieve_questions_by_type(t):
    questions_list = retrieve_questions()
    return list(filter(lambda x: x.type == t, questions_list))

def retrieve_questions_by_category(category):
    questions_list = retrieve_questions()
    return list(filter(lambda x: x.category == category, questions_list))

def retrieve_questions():
    db = client["Questions"]
    all_questions = db.all_questions.find()
    return [Question(**question) for question in all_questions]