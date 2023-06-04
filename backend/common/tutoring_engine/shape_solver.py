from backend.common.question_engine.graphics_question import TriangleQuestion, RectangleQuestion, CircleQuestion, Rectangle, Circle, Triangle
from typing import Union
import re
import traceback

class ShapeQuestionSolver:
    @staticmethod
    def __solve_triangle_question(question: TriangleQuestion):
        solution = []

        if isinstance(question.triangle, Triangle):
            triangle = question.triangle
        else:
            triangle = Triangle(**question.triangle)

        a = triangle.a
        b = triangle.b
        c = triangle.c
        
        if (question.topic == "area"):
            s = (a + b + c) / 2.0
            area_squared = s * (s - a) * (s - b) * (s - c)

            solution.append(f"To calculate the area of the triangle with side lengths ${a}$ cm, ${b}$ cm, ${c}$ cm, we can use Heron's Formula.")
            solution.append(f"The area of the a triangle with side lengths a, b, c are $A = \sqrt{{(s \\times (s - a) \\times (s - b) \\times (s - c))}}$, where $s = \\frac{{(a + b + c)}}{{2}}$")
            solution.append(f"In this case, the area is $A = \sqrt{{({s} \\times ({s} - {a}) \\times ({s} - {b}) \\times ({s} - {c}))}}$, where $s = \\frac{{({a} + {b} + {c})}}{{2}} = {s}$")
            solution.append(f"$A = \sqrt{{({area_squared})}}$")
            solution.append(f"$A = {triangle.calculate_area()}$")
            solution.append(f"Therefore, the area of the triangle is ${triangle.calculate_area():.3f}$ $cm^2$")


        return "<br />".join(solution)

    @staticmethod
    def __solve_rectangle_question(question: RectangleQuestion):
        solution = []
        if isinstance(question.rectangle, Rectangle):
            rectangle = question.rectangle
        else:
            rectangle = Rectangle(**question.rectangle)
        width = rectangle.width
        height = rectangle.height

        if (question.topic == "area"):
            solution.append(f"To calculate the area of the rectangle with with ${width}$ cm and height ${height}$ cm, we can multiply the width and height.")
            solution.append(f"The area of the rectangle can be computed using: $A = W * H$.")
            solution.append(f"$A = {width} * {height}$")
            solution.append(f"$A = {rectangle.calculate_area()}$")
            solution.append(f"Therefore, the area of the rectangle is ${rectangle.calculate_area():.3f}$ $cm^2$")

        return "<br />".join(solution)

    @staticmethod
    def __solve_circle_question(question: CircleQuestion):
        solution = []
        if isinstance(question.circle, Circle):
            circle = question.circle
        else:
            circle = Circle(**question.circle)
        radius = circle.radius

        if (question.topic == "area"):
            solution.append(f"To calculate the area of a circle with radius ${radius}$ cm, we can use the formula $A = \pi r^2$, where r is the radius of the circle.")
            solution.append(f"$A = \pi r^2$")
            solution.append(f"$A = \pi \\times {radius}^2$")
            solution.append(f"$A = {circle.calculate_area()}$")
            solution.append(f"Therefore, the area of the circle is ${circle.calculate_area():.3f}$ $cm^2$")
        elif (question.topic == "circumference"):
            solution.append(f"To calculate the circumference of a circle with radius ${radius}$ cm, we can use the formula $C = 2 \pi r$, where r is the radius of the circle.")
            solution.append(f"$C = 2 \pi r$")
            solution.append(f"$C = 2 \\times \pi \\times {radius}$")
            solution.append(f"$C = {circle.calculate_circumference()}$")
            solution.append(f"Therefore, the circumference of the circle is ${circle.calculate_circumference():.3f}$ cm")

        return "<br />".join(solution)
         
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
        
    @staticmethod
    def __generate_triangle_question(question: str):
        pattern = r'\d+(?:\.\d+)?'
        numbers = re.findall(pattern, question)
        numbers = list(map(int, numbers))
        A, B, C = numbers[0], numbers[1], numbers[2]
        if (A + B > C and A + C > B and B + C > A):
            triangle = Triangle(A, B, C)
            area = triangle.calculate_area()
            return TriangleQuestion(question, "trigonometry", triangle, "area", area, "N/A")

        return None
    
    @staticmethod
    def __generate_rectangle_question(question: str):
        pattern = r'\d+(?:\.\d+)?'
        numbers = re.findall(pattern, question)
        numbers = list(map(int, numbers))
        W, H = numbers[0], numbers[1]   
        rectangle = Rectangle(W, H)
        area = rectangle.calculate_area()

        return RectangleQuestion(question, "rectangle", rectangle, "area", area, "N/A")

    @staticmethod
    def __generate_circle_question(question: str, question_type: str):
        pattern = r'\d+(?:\.\d+)?'
        numbers = re.findall(pattern, question)
        numbers = list(map(int, numbers))
        RADIUS = numbers[0]
        circle = Circle(RADIUS)
        area = circle.calculate_area()
        return CircleQuestion(question, "circle", circle, question_type, area, "N/A")

    @staticmethod
    def parse_shape_question(question: str, tag: str):
        try:
            if tag == "triangle-area":
                triangleQuestion = ShapeQuestionSolver.__generate_triangle_question(question)
                if not triangleQuestion:
                    return "This question cannot be solved because the sum of any two side lengths must always be greater than the length of the third side."
                return ShapeQuestionSolver.solve_question(triangleQuestion)
            elif tag == "rectangle-area":
                rectangleQuestion = ShapeQuestionSolver.__generate_rectangle_question(question)
                return ShapeQuestionSolver.solve_question(rectangleQuestion)
            elif tag == "circle-area":
                circleQuestion = ShapeQuestionSolver.__generate_circle_question(question, "area")
                return ShapeQuestionSolver.solve_question(circleQuestion)
            elif tag == "circle-circumference":
                circleQuestion = ShapeQuestionSolver.__generate_circle_question(question, "circumference")
                return ShapeQuestionSolver.solve_question(circleQuestion)
        except:
            traceback.print_exc()
            return "Sorry! I am unable to solve this question."