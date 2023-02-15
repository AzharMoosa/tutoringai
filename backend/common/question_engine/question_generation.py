import json
from backend.common.question_engine.question import Question
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
    questions_json = json.loads(open(f"{__location__}/questions.json").read())
    return [Question(**question) for question in questions_json]
