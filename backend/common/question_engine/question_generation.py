from backend.common.question_engine.question import NumericalQuestion, MultipleChoiceQuestion, TrueOrFalseQuestion
from backend.resources.db import client
import random

db = client["Questions"]
question_bank = list(db["question_bank"].find())

def get_numerical_questions(questions):
    return [NumericalQuestion(**question) for question in questions if question["question_type"] == "numerical"]

def get_multiple_choice_questions(questions):
    return [MultipleChoiceQuestion(**question) for question in questions if question["question_type"] == "mcq"]

def get_true_or_false_questions(questions):
    return [TrueOrFalseQuestion(**question) for question in questions if question["question_type"] == "true-or-false"]

# Move To Chatroom DB
question_list = {}

class QuestionGenerator:
    @staticmethod
    def retrieve_questions_by_category(category):
        return [question_set for question_set in question_bank if question_set["category"] == category]
    
    @staticmethod
    def __generate_question_set_by_category(t):
        if (t in question_list):
            return question_list[t]

        question_options = QuestionGenerator.retrieve_questions_by_category(t)

        generated_questions = []

        for q_options in question_options:
            questions = q_options["questions"]
            numerical_questions = get_numerical_questions(questions)

            generated_questions.append(random.choice(numerical_questions))

            mcq_questions = get_multiple_choice_questions(questions)

            generated_questions.extend(random.choices(mcq_questions, k=2))

            true_or_false_questions = get_true_or_false_questions(questions)

            generated_questions.extend(random.choices(true_or_false_questions, k=2))
        
        random.shuffle(generated_questions)

        question_list[t] = generated_questions

        return generated_questions
    
    @staticmethod
    def retrieve_question_set_by_category(t):
        return QuestionGenerator.__generate_question_set_by_category(t)