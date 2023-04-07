import re
import json
from typing import List
from json import JSONEncoder
import os
from question import Question, QuestionEncoder, NumericalQuestion, MultipleChoiceQuestion
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
    def generate_questions():
        templates = QuestionEngine.__get_templates()

        for i, template in enumerate(templates):
            print(f"============ PARSING TEMPLATE {i} ============")
            # 1 - Parse Template & Generate Question Variants
            questions = QuestionEngine.__parse_template(template)

            print(f"Generated {len(questions)} Question Variants")

            # 2 - Pass All Variants Into MCQ Engine, True/False Engine & Fill In Blank Questions
            numerical_questions = [NumericalQuestion(question, template["category"], template["type"], answer) for question, answer in questions]

            print(f"Generated {len(numerical_questions)} Numerical Questions")

            # 3 - Combine All And Push To Question Bank
            QuestionEngine.__push_to_question_bank(numerical_questions)

            print(f"Successfully Added {len(numerical_questions)} Questions!")
            print(f"==== GENERATED QUESTIONS FOR TEMPLATE {i} ====")
    
if __name__ == "__main__":
    QuestionEngine.generate_questions()