from backend.common.question_engine.graphics_question import GraphicalQuestion
from backend.common.question_engine.question import Question
from backend.common.tutoring_engine.shape_solver import ShapeQuestionSolver
from backend.common.tutoring_engine.arithmetic_solver import ArithmeticSolver
from typing import Union

class TutoringEngine:
    @staticmethod
    def solve_question(question: Union[Question, GraphicalQuestion]):
        if (isinstance(question, GraphicalQuestion)):
            return ShapeQuestionSolver.solve_question(question)
        else:
            return ArithmeticSolver.solve_question(question)