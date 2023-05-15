from backend.common.question_engine.graphics_question import TriangleQuestion, RectangleQuestion, CircleQuestion, Triangle
from typing import Union

class ShapeQuestionSolver:
    @staticmethod
    def __solve_triangle_question(question: TriangleQuestion):
        if (question.topic == "area"):
            solution = []

            triangle = question.triangle
            a = triangle.a
            b = triangle.b
            c = triangle.c
            s = (a + b + c) / 2.0
            area_squared = s * (s - a) * (s - b) * (s - c)

            solution.append(f"To calculate the area of the triangle with side lengths {a} cm, {b} cm, {c} cm. We can use Heron's Formula.")
            solution.append(f"The area of the a triangle with side lengths a, b, c are A = sqrt(s * (s - a) * (s - b) * (s - c)), where s = (a + b + c) / 2")
            solution.append(f"In this case, the area is A = sqrt({s} * ({s} - {a}) * ({s} - {b}) * ({s} - {c})), where s = ({a} + {b} + {c}) / 2 = {s}")
            solution.append(f"A = sqrt({area_squared})")
            solution.append(f"A = {triangle.calculate_area()}")

            return "\n".join(solution)

    @staticmethod
    def __solve_rectangle_question(question: RectangleQuestion):
        pass

    @staticmethod
    def __solve_circle_question(question: CircleQuestion):
        pass

    @staticmethod
    def solve_question(question: Union[TriangleQuestion, RectangleQuestion, CircleQuestion]):
        if isinstance(question, TriangleQuestion):
            question.__class__ = TriangleQuestion
            return ShapeQuestionSolver.__solve_triangle_question(question)
        elif isinstance(question, RectangleQuestion):
            question.__class__ = RectangleQuestion
            return ShapeQuestionSolver.__solve_rectangle_question(question)
        elif isinstance(question, CircleQuestion):
            question.__class__ = CircleQuestion
            return ShapeQuestionSolver.__solve_circle_question(question)
        
if __name__ == "__main__":
    triangle = Triangle(1, 9, 9)
    area = triangle.calculate_area()
    triangle_question = TriangleQuestion("A triangle has side lengths 1cm, 9cm, 9cm. What is the area of the triangle?", "trigonometry", triangle, "area", area, "")

    circle_area_question = "A circle has radius 8cm. What is the area of the circle?"
    circle_circumference_question = "A circle has radius 3cm. What is the circumference of the circle?"
    rectangle_question = "A rectangle has width 3cm and height 3cm. What is the area of the rectangle?"

    print(ShapeQuestionSolver.solve_question(triangle_question))