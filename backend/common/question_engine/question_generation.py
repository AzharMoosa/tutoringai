import json
from backend.common.question_engine.question import NumericalQuestion, MultipleChoiceQuestion, TrueOrFalseQuestion
from backend.resources.db import client
import os

__location__ = os.path.realpath(os.path.join(
    os.getcwd(), os.path.dirname(__file__)))

def retrieve_questions_by_type(t):
    questions_list = retrieve_questions()
    return list(filter(lambda x: x.type == t, questions_list))

def retrieve_questions_by_category(category):
    questions_list = retrieve_questions()
    return {k : list(filter(lambda x: x.category == category, v)) for k, v in questions_list.items()}

def retrieve_questions():
    db = client["Questions"]
    question_bank = db["question_bank"].find()

    return {"numerical": [NumericalQuestion(**question) for question in question_bank if question["question_type"] == "numerical"], 
            "mcq": [MultipleChoiceQuestion(**question) for question in question_bank if question["question_type"] == "mcq"], 
            "true-or-false": [TrueOrFalseQuestion(**question) for question in question_bank if question["question_type"] == "true-or-false"] }
