import nltk
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

if __name__ == "__main__":
    print(AdditionSolver.solve_problem("A library currently has 10 books. The librarian orders 20 more books. How many books does the library have?"))
    print(SubtractionSolver.solve_problem("There were 25 birds sitting on a tree. 10 of them flew away. How many birds are left on the tree?"))