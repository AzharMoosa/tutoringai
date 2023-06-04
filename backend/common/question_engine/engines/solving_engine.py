import spacy
import re
from functools import reduce
nlp = spacy.load("en_core_web_sm")


class SolvingEngine:
    @staticmethod
    def __extract_key_information(text: str):
        information = {}
        doc = nlp(text)
        ents = [ent.text for ent in doc.ents if ent.label_ == "PERSON"]

        for person in set(ents):
            information[person] = 0

        return information
    
    @staticmethod
    def __find_in_order(lst, *args):
        if not args:
            return True
        if not lst:
            return False
        
        if args[0] == lst[0]:
            return SolvingEngine.__find_in_order(lst[1:], *args[1:])
        else:
            return SolvingEngine.__find_in_order(lst[1:], *args)
        
    def __solve_additive(question: str):
        # Add Base Information
        information = SolvingEngine.__extract_key_information(question)

        sentences = question.split(".")

        subject = None

        for sentence in sentences:
            sentence = sentence.strip()

            doc = nlp(sentence)
            numbers = [int(token.text) for token in doc if token.pos_ == "NUM"]
            pos = [token.pos_ for token in doc]

            if "?" in sentence:
                people = [token.text for token in doc if token.dep_ == "nsubj"]

                if len(people) != 1:
                    continue

                subject = people[0]

            if not numbers:
                continue

            if SolvingEngine.__find_in_order(pos, 'VERB', 'NUM', 'NOUN', 'ADP', 'PROPN'):
                people = [token.text for token in doc if token.dep_ in ("nsubj", "pobj")]
                
                if len(people) != 2:
                    continue

                information[people[0]] -= numbers[0]
                information[people[1]] += numbers[0]
            else:
                people = [token.text for token in doc if token.dep_ == "nsubj"]

                if len(people) != 1:
                    continue
            
                information[people[0]] += numbers[0]

        return information[subject] if subject else -1
    
    @staticmethod
    def __extract_numbers(question: str):
        numbers = re.findall(r'\d+', question)
        return [int(num) for num in numbers]
    
    @staticmethod
    def __solve_addition(question: str):
        numbers = SolvingEngine.__extract_numbers(question)
        return sum(numbers)

    @staticmethod
    def __solve_subtraction(question: str):
        numbers = SolvingEngine.__extract_numbers(question)
        return reduce(lambda x, y: x - y, numbers)

    @staticmethod
    def __solve_multiplication(question: str):
        numbers = SolvingEngine.__extract_numbers(question)
        return reduce(lambda x, y: x * y, numbers)

    @staticmethod
    def __solve_division(question: str):
        numbers = SolvingEngine.__extract_numbers(question)
        return reduce(lambda x, y: x / y, numbers)
    
    @staticmethod
    def solve(question: str, question_type: str) -> int:
        if question_type in ("additive"):
            return SolvingEngine.__solve_additive(question)
        elif question_type == "addition":
            return SolvingEngine.__solve_addition(question)
        elif question_type == "subtraction":
            return SolvingEngine.__solve_subtraction(question)
        elif question_type == "multiplication":
            return SolvingEngine.__solve_multiplication(question)
        elif question_type == "division":
            return SolvingEngine.__solve_division(question)

        raise Exception("Unknown Question Type")