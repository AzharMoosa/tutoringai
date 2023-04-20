from difflib import SequenceMatcher
import re
import spacy

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
    def solve(question: str, question_type: str) -> int:
        if (question_type == "additive"):
            return SolvingEngine.__solve_additive(question)

if __name__ == "__main__":
    q =  "John has 5 apples and his friend gave him 3 more. How many apples does John have now?"
    print(SolvingEngine.solve(q, "additive"))