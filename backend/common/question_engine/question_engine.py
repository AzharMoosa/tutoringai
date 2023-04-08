import re
import json
from typing import List, Tuple
from json import JSONEncoder
import os
from engines.text_to_question_engine import TextToQuestion
from engines.true_false_engine import TrueOrFalseEngine
from question import Question, QuestionEncoder, NumericalQuestion, MultipleChoiceQuestion, TrueOrFalseQuestion
from engines.maths_question_engine import MathsQuestions
from pymongo import MongoClient
from dotenv import load_dotenv
import os
load_dotenv()
client = MongoClient(os.getenv("MONGODB_URI"), serverSelectionTimeoutMS=5000)

__location__ = os.path.realpath(os.path.join(
    os.getcwd(), os.path.dirname(__file__)))


class QuestionEngine:
    @staticmethod
    def __push_to_question_bank(questions: List[Question]):
        questions_json = json.dumps(questions, indent=4, cls=QuestionEncoder)
        db = client["Questions"]
        question_bank = db["question_bank"]
        question_bank.drop()
        question_bank.insert_many(json.loads(questions_json))

    @staticmethod
    def __parse_template(template: dict) -> List[tuple]:
        # TODO: Remove Variant Number
        return MathsQuestions.generate_questions(template, 2)
    
    @staticmethod
    def __get_templates():
        # TODO: Add To DB And Fetch
        return [{ "type": "additive", "category": "arithmetic", "text" : "John, Joe, Sarah are in the park playing football and enjoying the sunny weather. They stop to have some lunch. John has 3 apples in his lunchbox. Joe has 2 apples in his lunchbox. Joe is feeling generous and gives 2 apples to John. Sarah also has 9 apples in her lunchbox. John is full and gives 4 apples to Sarah. How many apples does John now have?"
 }]
    
    @staticmethod
    def __remove_question_statement(text: str) -> str:
        return ".".join([line for line in text.split(".") if "?" not in line]) + "."

    
    @staticmethod
    def __get_multiple_choice_questions(text: str) -> dict:
        text = QuestionEngine.__remove_question_statement(text)
        return TextToQuestion.get_mcq_question(text)
    
    @staticmethod
    def get_true_false_questions(text: str) -> List[Tuple[str, str]]:
        text = QuestionEngine.__remove_question_statement(text)
        return sum([TrueOrFalseEngine.generate_false_options(line) for line in text.split(".") if line], [])
    
    @staticmethod
    def generate_questions():
        templates = QuestionEngine.__get_templates()

        for i, template in enumerate(templates):
            print(f"============ PARSING TEMPLATE {i} ============")
            # 1 - Parse Template & Generate Question Variants
            questions = QuestionEngine.__parse_template(template)

            print(f"Generated {len(questions)} Question Variants")

            # 2 - Pass All Variants Into MCQ Engine, True/False Engine & Fill In Blank Questions
            numerical_questions = [NumericalQuestion(question, template["category"], template["type"], answer) for question, answer in questions]
            mcq_questions = [MultipleChoiceQuestion(key, template["category"], template["type"], value[1], value[0], QuestionEngine.__remove_question_statement(text)) for text, _ in questions for key, value in QuestionEngine.__get_multiple_choice_questions(text).items()]
            true_or_false_questions = [TrueOrFalseQuestion(text, template["category"], template["type"], true_option, false_option) for text, _ in questions for true_option, false_option in QuestionEngine.get_true_false_questions(text)]

            print(f"Generated {len(numerical_questions)} Numerical Questions")
            print(f"Generated {len(mcq_questions)} MCQ Questions")
            print(f"Generated {len(true_or_false_questions)} True Or False Questions")

            # 3 - Combine All And Push To Question Bank
            QuestionEngine.__push_to_question_bank(numerical_questions)
            QuestionEngine.__push_to_question_bank(mcq_questions)
            QuestionEngine.__push_to_question_bank(true_or_false_questions)

            print(f"Successfully Added {len(numerical_questions) + len(mcq_questions) + len(true_or_false_questions)} Questions!")
            print(f"==== GENERATED QUESTIONS FOR TEMPLATE {i} ====")
    
if __name__ == "__main__":
    QuestionEngine.generate_questions()