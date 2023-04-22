from backend.common.tutoring_engine.arithmetic_solver import AdditionSolver, SubtractionSolver, MultiplicationSolver, DivisionSolver
import unittest

class TestArithmeticSolvers(unittest.TestCase):
    def test_solve_addition_problem_correctly_one(self):
        worded_problem = "John has 5 apples and his friend gave him 3 more. How many apples does John have now?"
        answer = AdditionSolver.solve_problem(worded_problem)
        self.assertEqual(answer, 8)

    def test_solve_addition_problem_correctly_two(self):
        worded_problem = "A library currently has 10 books. The librarian orders 20 more books. How many books does the library have?"
        answer = AdditionSolver.solve_problem(worded_problem)
        self.assertEqual(answer, 30)

    def test_solve_subtraction_problem_correctly_one(self):
        worded_problem = "There are 25 birds that are currently sitting on a tree. It starts to rain and 10 of them fly away. How many birds are there left on the tree?"
        answer = SubtractionSolver.solve_problem(worded_problem)
        self.assertEqual(answer, 15)

    def test_solve_subtraction_problem_correctly_two(self):
        worded_problem = "A boy had 8 marbles and he gave 3 to his friend. How many marbles does he have now?"
        answer = SubtractionSolver.solve_problem(worded_problem)
        self.assertEqual(answer, 5)

    def test_solve_multiplication_problem_correctly_one(self):
        worded_problem = "John has 5 boxes of chocolates, each box contains 10 chocolates. How many chocolates does John have in total?"
        answer = MultiplicationSolver.solve_problem(worded_problem)
        self.assertEqual(answer, 50)

    def test_solve_multiplication_problem_correctly_two(self):
        worded_problem = "A school has 4 classes, each class has 25 students. How many students are there in total at the school?"
        answer = MultiplicationSolver.solve_problem(worded_problem)
        self.assertEqual(answer, 100)

    def test_solve_division_problem_correctly_one(self):
        worded_problem = "There are 24 cookies to share equally among 6 children. How many cookies will each child get?"
        answer = DivisionSolver.solve_problem(worded_problem)
        self.assertAlmostEqual(answer, 4.0)

    def test_solve_division_problem_correctly_two(self):
        worded_problem = "A teacher has 36 pencils to share equally among 9 students. How many pencils will each student get?"
        answer = DivisionSolver.solve_problem(worded_problem)
        self.assertAlmostEqual(answer, 4.0)

if __name__ == '__main__':
    unittest.main()