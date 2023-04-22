import nltk
import math
nltk.download('averaged_perceptron_tagger')
from nltk.tokenize import word_tokenize

class AdditionSolver:
    @staticmethod
    def solve_problem(word_problem: str) -> int:
        tokens = word_tokenize(word_problem)
        part_of_speech_tags = nltk.pos_tag(tokens)
        numbers = [int(n) for n, tag in part_of_speech_tags if tag == 'CD']
        return sum(numbers)

    @staticmethod
    def solve_problem_with_steps(word_problem: str) -> int:
        pass

class SubtractionSolver:
    @staticmethod
    def solve_problem(word_problem: str) -> int:
        tokens = word_tokenize(word_problem)
        part_of_speech_tags = nltk.pos_tag(tokens)
        numbers = [int(n) for n, tag in part_of_speech_tags if tag == 'CD']
        return numbers[0] - sum(numbers[1:])

    @staticmethod
    def solve_problem_with_steps(word_problem: str) -> int:
        pass

class MultiplicationSolver:
    @staticmethod
    def solve_problem(word_problem: str) -> int:
        tokens = word_tokenize(word_problem)
        part_of_speech_tags = nltk.pos_tag(tokens)
        numbers = [int(n) for n, tag in part_of_speech_tags if tag == 'CD']
        return math.prod(numbers)

    @staticmethod
    def solve_problem_with_steps(word_problem: str) -> int:
        pass

class DivisionSolver:
    @staticmethod
    def solve_problem(word_problem: str) -> int:
        tokens = word_tokenize(word_problem)
        part_of_speech_tags = nltk.pos_tag(tokens)
        numbers = [int(n) for n, tag in part_of_speech_tags if tag == 'CD']
        return numbers[0] / numbers[1]

    @staticmethod
    def solve_problem_with_steps(word_problem: str) -> int:
        pass

if __name__ == "__main__":
    print(AdditionSolver.solve_problem("A library currently has 10 books. The librarian orders 20 more books. How many books does the library have?"))
    print(SubtractionSolver.solve_problem("A boy had 8 marbles and he gave 3 to his friend. How many marbles does he have now?"))
    print(MultiplicationSolver.solve_problem("A school has 4 classes, each class has 25 students. How many students are there in total at the school?"))
    print(DivisionSolver.solve_problem("There are 24 cookies to share equally among 6 children. How many cookies will each child get?"))