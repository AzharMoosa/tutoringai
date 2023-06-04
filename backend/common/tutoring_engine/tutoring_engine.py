from backend.common.question_engine.graphics_question import GraphicalQuestion
from backend.common.question_engine.question import Question
from backend.common.tutoring_engine.shape_solver import ShapeQuestionSolver
from backend.common.tutoring_engine.arithmetic_solver import ArithmeticSolver
import re
from typing import Union

ARITHMETIC_PATTERN = r"\b\d+\s*[-+*/]\s*\d+\b"

class TutoringEngine:
    @staticmethod
    def solve_question(question: Union[Question, GraphicalQuestion]):
        if (isinstance(question, GraphicalQuestion)):
            return ShapeQuestionSolver.solve_question(question)
        else:
            return ArithmeticSolver.solve_question(question)
        
    @staticmethod
    def solve_simple_arithmetics(text: str):
        equations = re.findall(ARITHMETIC_PATTERN, text)

        result = []

        for equation in equations:
            equation_str = equation.strip()
            ans = eval(equation_str)
            solution = f"The answer to {equation_str} is {str(ans)}"
            result.append(solution)

        return "<br />".join(result)

    @staticmethod
    def contains_simple_arithmetics(text: str):
        equations = re.findall(ARITHMETIC_PATTERN, text)

        return len(equations) > 0