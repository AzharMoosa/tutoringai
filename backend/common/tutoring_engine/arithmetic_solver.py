import nltk
import math
nltk.download('averaged_perceptron_tagger')
from nltk.tokenize import word_tokenize
import spacy

nlp = spacy.load("en_core_web_sm")

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

class AdditiveSolver:
    @staticmethod
    def __extract_key_information(text: str) -> dict:
        information = {}
        
        # Find All Names In Text
        doc = nlp(text)
        ents = [ent.text for ent in doc.ents if ent.label_ == "PERSON"]

        # Initialise Count Of Object To One
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
            return AdditiveSolver.__find_in_order(lst[1:], *args[1:])
        else:
            return AdditiveSolver.__find_in_order(lst[1:], *args)
        
    @staticmethod
    def solve_problem(word_problem: str) -> int:
        # Analyze Text & Find Key Information
        information = AdditiveSolver.__extract_key_information(word_problem)

        sentences = word_problem.split(".")

        subject = None

        for sentence in sentences:
            sentence = sentence.strip()

            doc = nlp(sentence)
            numbers = [int(token.text) for token in doc if token.pos_ == "NUM"]
            pos = [token.pos_ for token in doc]
            
            # Find Subject In Question
            if "?" in sentence:
                people = [token.text for token in doc if token.dep_ == "nsubj"]

                if len(people) != 1:
                    continue

                subject = people[0]

            if not numbers:
                continue

            subtraction_pattern = ['VERB', 'NUM', 'NOUN', 'ADP', 'PROPN']

            is_subtraction = AdditiveSolver.__find_in_order(pos, *subtraction_pattern)

            if is_subtraction:
                # Find Two People In Sentence
                people = [token.text for token in doc if token.dep_ in ("nsubj", "pobj")]
                
                if len(people) != 2:
                    continue
                
                # Assuming Sentence Of Form: <PERSON_ONE> gives <NUMBER> <OBJECT> to <PERSON_TWO>
                information[people[0]] -= numbers[0]
                information[people[1]] += numbers[0]
            else:
                people = [token.text for token in doc if token.dep_ == "nsubj"]

                if len(people) != 1:
                    continue

                # Assuming Sentence Of Form: <PERSON> has <NUM> <OBJECT>
                information[people[0]] += numbers[0]
        
        return information[subject] if subject else -1

    @staticmethod
    def solve_problem_with_steps(word_problem: str) -> int:
        pass

if __name__ == "__main__":
    # print(AdditionSolver.solve_problem("A library currently has 10 books. The librarian orders 20 more books. How many books does the library have?"))
    # print(SubtractionSolver.solve_problem("A boy had 8 marbles and he gave 3 to his friend. How many marbles does he have now?"))
    # print(MultiplicationSolver.solve_problem("A school has 4 classes, each class has 25 students. How many students are there in total at the school?"))
    # print(DivisionSolver.solve_problem("There are 24 cookies to share equally among 6 children. How many cookies will each child get?"))
    print(AdditiveSolver.solve_problem("John, Joe, Sarah are in the park playing football and enjoying the sunny weather. They stop to have some lunch. John has 3 apples in his lunchbox. Joe has 2 apples in his lunchbox. Joe is feeling generous and gives 2 apples to John. Sarah also has 9 apples in her lunchbox. John is full and gives 4 apples to Sarah. How many apples does John now have?"))
    print(AdditiveSolver.solve_problem("John, Joe, Sarah are hungry and decide they want to go eat some lunch. They go to their favorite restaurant nearby and decide to order pizza. John takes 2 slices of pizza. Joe loves pizza and decides to take 4 slices of pizza. Sarah then takes the final 2 pizzas. Joe is feeling generous and gives 1 pizza to John. Sarah is also feeling generous and gives 1 pizza to John. How many pizzas did John eat?"))