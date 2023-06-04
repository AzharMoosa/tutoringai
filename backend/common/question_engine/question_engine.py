import re
import random
import json
from typing import List, Tuple
from json import JSONEncoder
import os
from backend.common.question_engine.question import Question, QuestionEncoder, NumericalQuestion, MultipleChoiceQuestion, TrueOrFalseQuestion, QuestionSet
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import traceback

load_dotenv()
client = MongoClient(os.getenv("MONGODB_URI"), serverSelectionTimeoutMS=5000)

__location__ = os.path.realpath(os.path.join(
    os.getcwd(), os.path.dirname(__file__)))


class QuestionEngine:
    @staticmethod
    def __push_to_question_bank(questions: List[Question]) -> None:
        questions_json = json.dumps(questions, indent=4, cls=QuestionEncoder)
        db = client["Questions"]
        question_bank = db["question_bank"]
        question_bank.insert_many(json.loads(questions_json))

    @staticmethod
    def __parse_template(template: dict) -> List[tuple]:
        return MathsQuestions.generate_questions(template, 2)
    
    @staticmethod
    def __get_templates():
        with open(f"{__location__}/questions.json", 'r') as f:
            return json.load(f)
    
    @staticmethod
    def __remove_question_statement(text: str) -> str:
        return ".".join([line for line in text.split(".") if "?" not in line]) + "."

    
    @staticmethod
    def __get_multiple_choice_questions(text: str) -> dict:
        text = QuestionEngine.__remove_question_statement(text)
        return TextToQuestion.get_mcq_question(text)
    
    @staticmethod
    def get_true_false_questions(text: str) -> List[Tuple[List[str], str]]:
        text = QuestionEngine.__remove_question_statement(text)
        line = random.choice([line for line in text.split(".") if line])
        return TrueOrFalseEngine.generate_false_options(line) if line else []
    
    @staticmethod
    def generate_questions(include_numerical_questions: bool = True, include_mcq_questions: bool = True, include_true_or_false_questions: bool = True, clear_db: bool = False):
        templates = QuestionEngine.__get_templates()

        if clear_db:
            db = client["Questions"]
            question_bank = db["question_bank"]
            question_bank.drop()

        for i, template in enumerate(templates):
            try:
                print(f"============ PARSING TEMPLATE {i} ============")
                # 1 - Parse Template & Generate Question Variants
                question_variants = QuestionEngine.__parse_template(template)

                print(f"Generated {len(question_variants)} Question Variants")

                question_sets = []

                for questions in question_variants:
                    # 2 - Pass All Variants Into MCQ Engine, True/False Engine & Fill In Blank Questions
                    try:
                        numerical_questions = [NumericalQuestion(question, template["category"], template["type"], answer) for question, answer in questions] if include_numerical_questions else []
                    except:
                        traceback.print_exc()
                        print(f"Could Not Add Numerical Questions For Template: {i}")
                        numerical_questions = []

                    try:    
                        mcq_questions = [MultipleChoiceQuestion(key, template["category"], template["type"], value[1], value[0], QuestionEngine.__remove_question_statement(text)) for text, _ in questions for key, value in QuestionEngine.__get_multiple_choice_questions(text).items()] if include_mcq_questions else []
                    except:
                        traceback.print_exc()
                        print(f"Could Not Add MCQ For Template: {i}")
                        mcq_questions = []

                    try:
                        true_or_false_questions = []

                        if include_true_or_false_questions:
                            for text, _ in questions:
                                options = QuestionEngine.get_true_false_questions(text)
                                for true_options, false_option in options:
                                    answer = random.choice([True, False])
                                    if (answer):
                                        statement = random.choice(true_options)
                                    else:
                                        statement = false_option
                                    true_or_false_questions.append(TrueOrFalseQuestion(QuestionEngine.__remove_question_statement(text), template["category"], template["type"], answer, statement))
                    except:
                        traceback.print_exc()
                        print(f"Could Not Add True Or False Questions For Template: {i}")
                        true_or_false_questions = []

                    question_sets.append(QuestionSet(numerical_questions + mcq_questions + true_or_false_questions, template["category"]))

                print(f"Generated {len(question_sets)} Question Sets")

                # 3 - Push To Question Bank
                QuestionEngine.__push_to_question_bank(question_sets)

                print(f"Successfully Added {len(question_sets)} Questions Sets!")
                print(f"==== GENERATED QUESTIONS FOR TEMPLATE {i} ====")
            except:
                traceback.print_exc()
                print(f"Could Not Parse Template: {template}")
                continue
    
if __name__ == "__main__":
    include_numerical_questions = True
    include_mcq_questions = True
    include_true_or_false_questions = True
    clear_db = False

    if include_true_or_false_questions:
        from backend.common.question_engine.engines.true_false_engine import TrueOrFalseEngine

    if include_numerical_questions or include_true_or_false_questions:
        from backend.common.question_engine.engines.maths_question_engine import MathsQuestions

    if include_mcq_questions:
        from backend.common.question_engine.engines.text_to_question_engine import TextToQuestion
        from backend.common.question_engine.engines.maths_question_engine import MathsQuestions

    QuestionEngine.generate_questions(include_numerical_questions=include_numerical_questions, 
                                      include_mcq_questions=include_mcq_questions, 
                                      include_true_or_false_questions=include_true_or_false_questions, 
                                      clear_db=clear_db)
