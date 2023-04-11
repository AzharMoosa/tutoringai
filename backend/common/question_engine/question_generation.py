from backend.common.question_engine.question import NumericalQuestion, MultipleChoiceQuestion, TrueOrFalseQuestion
from backend.resources.db import client


db = client["Questions"]
question_bank = list(db["question_bank"].find())

def numerical_questions():
    return [NumericalQuestion(**question) for question in question_bank if question["question_type"] == "numerical"]

def multiple_choice_questions():
    return [MultipleChoiceQuestion(**question) for question in question_bank if question["question_type"] == "mcq"]

def true_or_false_questions():
    return [TrueOrFalseQuestion(**question) for question in question_bank if question["question_type"] == "true-or-false"]

questions_list = { "numerical": numerical_questions(), "mcq": multiple_choice_questions(), "true-or-false": true_or_false_questions() }

class QuestionGenerator:
    @staticmethod
    def retrieve_questions_by_type(t):
        return {k : list(filter(lambda x: x.type == t, v)) for k, v in questions_list.items()}

    @staticmethod
    def retrieve_questions_by_category(category):
        return {k : list(filter(lambda x: x.category == category, v)) for k, v in questions_list.items()}
    
    @staticmethod
    def retrieve_question_set_by_category(t):
        question_options = QuestionGenerator.retrieve_questions_by_category(t)

        return question_options["numerical"] + question_options["mcq"] + question_options["true-or-false"]
