from typing import Tuple, List
import torch
from backend.common.question_engine.engines.keyword_extraction_engine import KeywordExtraction
from backend.common.question_engine.engines.summarization_engine import TextSummarization
from sense2vec import Sense2Vec
import random
from rapidfuzz.distance import Levenshtein
from backend.common.question_engine.engines.mcq_engine import MCQEngine
import nltk
import os
import traceback
import requests
from dotenv import load_dotenv
load_dotenv()

nltk.download('omw-1.4')

__location__ = os.path.realpath(os.path.join(
    os.getcwd(), os.path.dirname(__file__)))

s2v = Sense2Vec().from_disk(f"{__location__}/s2v")

class TextToQuestion:
    @staticmethod
    def generate_question_api(context: str, answer: str):
        BASE_URL = os.getenv("MARC_API_URI")
        API_URL = f"{BASE_URL}/generate-question"
        payload = { "context": str(context), "answer": str(answer) }
        try:
            response = requests.post(API_URL, json=payload).json()
            return response["question"]
        except:
            traceback.print_exc()
            return []

    @staticmethod
    def __filter_same_sense(sense: str, words: List[str]) -> List[str]:
        """
        Filters a list of words using a base sense.

        Arguments:
            sense {str} The base sense to use
            words {List[str]} The list of words to filter

        Returns:
            {List[str]} The input ids and the attention mask
        """
        def process_word(word: str) -> str:
            return word[0].split("|")[0].replace("_", " ").title().strip()

        sense = sense.split("|")[1]
        
        return [process_word(word) for word in words if word[0].split("|")[1] == sense]

    @staticmethod
    def __maximum_similarity_score(word: str, words: List[str]):
        """
        Retrieves the maximum similarity score using a word and
        a list of words.

        Arguments:
            word {str} The base word to compare to
            words {List[str]} The list of words to compare to

        Returns:
            {List[str]} The input ids and the attention mask
        """
        return max([Levenshtein.normalized_distance(w.lower(), word.lower()) for w in words])

    @staticmethod
    def __generate_distractors_sense2vec(word: str, question: str, n=40):
        best_sense = s2v.get_best_sense(word, senses=["NOUN", "PERSON", "PRODUCT", "LOC", "ORG", "EVENT", "NORP", "WORK OF ART", "FAC", "GPE", "NUM", "FACILITY"])
        most_similar = TextToQuestion.__filter_same_sense(best_sense, s2v.most_similar(best_sense, n=n))

        threshold = 0.6
        distractors = [word]
        question_token = question.split()

        for word in most_similar:
            if TextToQuestion.__maximum_similarity_score(word, distractors) < threshold and word not in distractors and distractors not in question_token:
                distractors.append(word)
            
        return distractors[1:]
    
    @staticmethod
    def get_mcq_question(text: str, options: int = 4, type: str="transformer") -> dict:
        """
        Generates MCQ questions for a text input.

        Arguments:
            text {str} The base word to compare to
            options {int} The number of options to use in the MCQ
            type {str} The type of method used to generate distractors

        Returns:
            {dict} The mapping of a question to the distractors and the answer
                   to the MCQ question.
        """
        question_list = TextToQuestion.get_question(text)
        mcq_mapping = {}
        for question, answer in question_list:
            if type == "wordnet":
                distractors = MCQEngine.generate_distractors_wordnet(answer)
            elif type == "sense2vec":
                distractors = MCQEngine.generate_distractors_sense2vec(answer)
            elif type == "transformer":
                distractors = MCQEngine.generate_distractors_transformer(answer)
            else:
                distractors = []

            distractors = [answer.capitalize()] + distractors[:options-1]
            random.shuffle(distractors)
            mcq_mapping[question] = (distractors, answer.capitalize())

        return mcq_mapping

    @staticmethod
    def get_question(context: str) -> List[Tuple[str, str]]:
        """
        Generates questions using a given text input

        Arguments:
            context {str} The input text used to generate questions from

        Returns:
            {List[Tuple[str, str]]} A list of questions and answers
        """
        summarized_text = TextSummarization.summarize(context)
        keywords = KeywordExtraction.get_keywords(context)
        question_list = []

        for keyword in keywords:
            questions = TextToQuestion.generate_question_api(summarized_text, keyword)
            if not questions:
                continue
            question = random.choice(questions).replace("question:", "").strip()
            question_list.append((question, keyword))

        return question_list