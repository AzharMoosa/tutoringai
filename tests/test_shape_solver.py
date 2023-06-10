import unittest
from backend.common.tutoring_engine.shape_solver import ShapeQuestionSolver
from backend.common.question_engine.graphics_question import TriangleQuestion, Triangle, RectangleQuestion, Rectangle, Circle, CircleQuestion

class TestShapeSolver(unittest.TestCase):
    def test_invalid_triangle(self):
        attempted_solution = ShapeQuestionSolver.parse_shape_question("Calculate the area of the triangle with side lengths 1, 2, 3", "triangle-area")
        self.assertEqual(attempted_solution,  "This question cannot be solved because the sum of any two side lengths must always be greater than the length of the third side.")

    def test_solve_triangle_question(self):
        triangle = Triangle(10, 11, 12)
        triangle_question = TriangleQuestion("-", "-", triangle, "area", triangle.calculate_area(), "-")
        solution = ShapeQuestionSolver.solve_question(triangle_question)
        correct_solution = "To calculate the area of the triangle with side lengths $10$, $11$, $12$, we can use Heron's Formula.<br />The area of the a triangle with side lengths a, b, c are $A = \sqrt{(s \\times (s - a) \\times (s - b) \\times (s - c))}$, where $s = \\frac{(a + b + c)}{2}$<br />In this case, the area is $A = \sqrt{(16.5 \\times (16.5 - 10) \\times (16.5 - 11) \\times (16.5 - 12))}$, where $s = \\frac{(10 + 11 + 12)}{2} = 16.5$<br />$A = \sqrt{(2654.4375)}$<br />$A = 51.521233486786784$<br />Therefore, the area of the triangle is $51.521$"
        self.assertEqual(solution, correct_solution)

    def test_solve_rectangle_question(self):
        rectangle = Rectangle(10, 5)
        rectangle_question = RectangleQuestion("-", "-", rectangle, "area", rectangle.calculate_area(), "-")
        solution = ShapeQuestionSolver.solve_question(rectangle_question)
        correct_solution = "To calculate the area of the rectangle with with $10$ and height $5$, we can multiply the width and height.<br />The area of the rectangle can be computed using: $A = W * H$.<br />$A = 10 * 5$<br />$A = 50$<br />Therefore, the area of the rectangle is $50.000$"
        self.assertEqual(solution, correct_solution)

    def test_solve_circle_area_question(self):
        circle = Circle(5)
        circle_question = CircleQuestion("-", "-", circle, "area", circle.calculate_area(), "-")
        solution = ShapeQuestionSolver.solve_question(circle_question)
        correct_solution = "To calculate the area of a circle with radius $5$, we can use the formula $A = \pi r^2$, where r is the radius of the circle.<br />$A = \pi r^2$<br />$A = \pi \\times 5^2$<br />$A = 78.53981633974483$<br />Therefore, the area of the circle is $78.540$"
        self.assertEqual(solution, correct_solution)

    def test_solve_circle_circumference_question(self):
        circle = Circle(3)
        circle_question = CircleQuestion("-", "-", circle, "circumference", circle.calculate_area(), "-")
        solution = ShapeQuestionSolver.solve_question(circle_question)
        correct_solution = "To calculate the circumference of a circle with radius $3$, we can use the formula $C = 2 \pi r$, where r is the radius of the circle.<br />$C = 2 \pi r$<br />$C = 2 \\times \pi \\times 3$<br />$C = 18.84955592153876$<br />Therefore, the circumference of the circle is $18.850$"
        self.assertEqual(solution, correct_solution)

if __name__ == '__main__':
    unittest.main()