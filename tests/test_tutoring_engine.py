import unittest
from backend.common.tutoring_engine.tutoring_engine import TutoringEngine

class TestShapeSolver(unittest.TestCase):
    def test_simple_arithmetics(self):
        solution = TutoringEngine.solve_simple_arithmetics("What is 1+4?")
        self.assertEqual(solution, "The answer to 1+4 is 5")

    def test_simple_arithmetics_multiple(self):
        solution = TutoringEngine.solve_simple_arithmetics("What is 1+4? What is 4*5?")
        self.assertEqual(solution, "The answer to 1+4 is 5<br />The answer to 4*5 is 20")

    def test_contains_simple_arithmetics_true(self):
        contains = TutoringEngine.contains_simple_arithmetics("What is 1+4? What is 4*5?")
        self.assertTrue(contains)
    
    def test_contains_simple_arithmetics_false(self):
        contains = TutoringEngine.contains_simple_arithmetics("This is just a regular string?")
        self.assertFalse(contains)

if __name__ == '__main__':
    unittest.main()