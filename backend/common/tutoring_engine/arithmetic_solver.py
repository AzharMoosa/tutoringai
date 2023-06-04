import os
import requests
from typing import Union
from dotenv import load_dotenv
from backend.common.question_engine.question import NumericalQuestion, MultipleChoiceQuestion, TrueOrFalseQuestion

load_dotenv()

class ArithmeticSolver:
    @staticmethod
    def __solve_numerical_question(question: NumericalQuestion):
        BASE_URL = os.getenv("MARC_API_URI")
        API_URL = f"{BASE_URL}/solve-math-problem"
        payload = { "question": str(question) }
        try:
            response = requests.post(API_URL, json=payload).json()
            return response["answer"]
        except:
            return "Sorry! I am unable to solve this problem."

    @staticmethod
    def solve_question(question: Union[NumericalQuestion, MultipleChoiceQuestion, TrueOrFalseQuestion]):
        if (isinstance(question, NumericalQuestion)):
            question.__class__ = NumericalQuestion
            return ArithmeticSolver.__solve_numerical_question(question)
        else:
            return ""

        