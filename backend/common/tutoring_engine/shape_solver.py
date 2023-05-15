from backend.common.question_engine.graphics_question import TriangleQuestion, RectangleQuestion, CircleQuestion
from typing import Union

class ShapeQuestionSolver:
    @staticmethod
    def __solve_triangle_question(question: TriangleQuestion):
        solution = []
        triangle = question.triangle
        a = triangle.a
        b = triangle.b
        c = triangle.c
        
        if (question.topic == "area"):
            s = (a + b + c) / 2.0
            area_squared = s * (s - a) * (s - b) * (s - c)

            solution.append(f"To calculate the area of the triangle with side lengths {a} cm, {b} cm, {c} cm, we can use Heron's Formula.")
            solution.append(f"The area of the a triangle with side lengths a, b, c are A = sqrt(s * (s - a) * (s - b) * (s - c)), where s = (a + b + c) / 2")
            solution.append(f"In this case, the area is A = sqrt({s} * ({s} - {a}) * ({s} - {b}) * ({s} - {c})), where s = ({a} + {b} + {c}) / 2 = {s}")
            solution.append(f"A = sqrt({area_squared})")
            solution.append(f"A = {triangle.calculate_area()}")
            solution.append(f"Therefore, the area of the triangle is {triangle.calculate_area():.3f} cm²")


        return "\n".join(solution)

    @staticmethod
    def __solve_rectangle_question(question: RectangleQuestion):
        solution = []
        rectangle = question.rectangle
        width = rectangle.width
        height = rectangle.height

        if (question.topic == "area"):
            solution.append(f"To calculate the area of the rectangle with with {width} cm and height {height} cm, we can multiply the width and height.")
            solution.append(f"The area of the rectangle can be computed using: A = W * H")
            solution.append(f"A = {width} * {height}")
            solution.append(f"A = {rectangle.calculate_area()}")
            solution.append(f"Therefore, the area of the rectangle is {rectangle.calculate_area():.3f} cm²")

        return "\n".join(solution)

    @staticmethod
    def __solve_circle_question(question: CircleQuestion):
        solution = []
        circle = question.circle
        radius = circle.radius

        if (question.topic == "area"):
            solution.append(f"To calculate the area of a circle with radius {radius} cm, we can use the formula A = πr², where r is the radius of the circle.")
            solution.append(f"A = πr²")
            solution.append(f"A = π * {radius}²")
            solution.append(f"A = {circle.calculate_area()}")
            solution.append(f"Therefore, the area of the circle is {circle.calculate_area():.3f} cm²")
        elif (question.topic == "circumference"):
            solution.append(f"To calculate the circumference of a circle with radius {radius} cm, we can use the formula C = 2πr, where r is the radius of the circle.")
            solution.append(f"C = 2πr")
            solution.append(f"C = 2 * π * {radius}")
            solution.append(f"C = {circle.calculate_circumference()}")
            solution.append(f"Therefore, the circumference of the circle is {circle.calculate_circumference():.3f} cm")

        return "\n".join(solution)
         
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