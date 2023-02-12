import json
from backend.common.question_engine.question import Question
import os

__location__ = os.path.realpath(os.path.join(
    os.getcwd(), os.path.dirname(__file__)))


def retrieve_questions():
    questions_json = json.loads(open(f"{__location__}/questions.json").read())
    return [Question(**question) for question in questions_json]
