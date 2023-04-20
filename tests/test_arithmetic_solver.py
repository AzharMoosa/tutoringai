from backend.common.tutoring_engine.arithmetic_solver import AdditionSolver
import unittest

class TestAdditionSolver(unittest.TestCase):
    def test_solve_correctly_one(self):
        worded_problem = "John has 5 apples and his friend gave him 3 more. How many apples does John have now?"
        answer = AdditionSolver.solve_problem(worded_problem)
        self.assertEqual(answer, 8)

    def test_solve_correctly_two(self):
        worded_problem = "A library currently has 10 books. The librarian orders 20 more books. How many books does the library have?"
        answer = AdditionSolver.solve_problem(worded_problem)
        self.assertEqual(answer, 30)

if __name__ == '__main__':
    unittest.main()