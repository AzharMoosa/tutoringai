import random
from textwrap import dedent
from itertools import pairwise

class TutoringResponse:
    def __init__(self, answer, explainations):
        self.answer = answer
        self.explainations = explainations

class ArithmeticEngine:
    @staticmethod
    def parse_numbers(expression, delimiter):
        return list(map(int, expression.split(delimiter)))
    
    @staticmethod
    def construct_addition_explaination(o, numbers):
        def singular_or_plural(num):
            return o[0] if num == 1 else o[1]
        
        def generate_statement(prev, next):
            return dedent(f"""\
                Then you take {next} {singular_or_plural(next)} to get a total of
                {prev + next} {singular_or_plural(prev + next)}.""").replace("\n", " ")
        
        def generate_pairwise_statement():
            return ' '.join([generate_statement(prev, next) for prev, next in pairwise(numbers)])
        
        def generate_starter_statement():
            return random.choice([f"Imagine you have a bag of {o[1]}.", f"Lets take an example. Imagine you have a bag of {o[1]}.", f"An example that might help you understand this involves a bag of {o[1]}."])
                
        return dedent(f"""\
                    {generate_starter_statement()}
                    You first take {numbers[0]} {singular_or_plural(numbers[0])} out of the bag.
                    {generate_pairwise_statement()}""").replace("\n", " ")
    
    @staticmethod
    def addition_explainations(expression):
        numbers = ArithmeticEngine.parse_numbers(expression, "+")
        if len(numbers) < 2:
            raise Exception("Invalid Expression")
        object_example = [("candy", "candies"), ("orange", "oranges"), ("sweet", "sweets"), ("apple", "apples")]
        word_explainations = [ArithmeticEngine.construct_addition_explaination(o, numbers) for o in object_example]
        return word_explainations

    @staticmethod
    def subtraction_explainations(expression):
        numbers = ArithmeticEngine.parse_numbers(expression, "-")

    @staticmethod
    def multiplication_explainations(expression):
        numbers = ArithmeticEngine.parse_numbers(expression, "*")

    @staticmethod
    def division_explainations(expression):
        numbers = ArithmeticEngine.parse_numbers(expression, "/")

    @staticmethod
    def compute(expression):
        answer = eval(expression)

        if '+' in expression:
            return TutoringResponse(answer, ArithmeticEngine.addition_explainations(expression))
        elif '-' in expression:
            return TutoringResponse(answer, ArithmeticEngine.subtraction_explainations(expression))
        elif '*' in expression:
            return TutoringResponse(answer, ArithmeticEngine.multiplication_explainations(expression))
        elif '/' in expression:
            return TutoringResponse(answer, ArithmeticEngine.division_explainations(expression))
        else:
            raise Exception("Invalid Expression")

if __name__ == "__main__":
    response = ArithmeticEngine.compute("1+3+5+2")
    print(response.answer)
    print(response.explainations)
