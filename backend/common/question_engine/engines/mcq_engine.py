from nltk.corpus import wordnet
from typing import List
import nltk
import re
import random
import json
import requests
from collections import OrderedDict
import string
from sense2vec import Sense2Vec
from rapidfuzz.distance import Levenshtein

nltk.download("wordnet")


class MCQEngine:
    def __init__(self, question: str, answer: str) -> None:
        self.question = question
        self.answer = answer
        self.s2v = Sense2Vec().from_disk("s2v")

    def __get_synset(self, word: str):
        return wordnet.synsets(word, "n")

    def generate_distractors_wordnet(self) -> List[List[str]]:
        distractors = []

        answer = self.answer.lower()
        synset = self.__get_synset(answer)
        answer = answer.replace(" ", "_")

        for s in synset:
            distractor = []
            # Generate Hypernyms
            hypernym = s.hypernyms()

            if len(hypernym) == 0:
                return distractors

            hyponyms = hypernym[0].hyponyms()

            for h in hyponyms:
                name = h.lemmas()[0].name()
                if name != self.answer.lower():
                    name = name.replace(" ", "_")
                    name = " ".join(w.capitalize() for w in name.split())
                    if name and name not in distractors:
                        distractor.append(name)

            distractors.append(distractor)

        return distractors

    def __get_concept_net_graph(self, url: str) -> dict:
        return requests.get(url).json()

    def generate_distractors_conceptnet(self) -> List[str]:
        distractors = []

        answer = self.answer.lower()
        answer = answer.replace(" ", "_")
        CONCEPT_NET_URL_ONE = f"http://api.conceptnet.io/query?node=/c/en/{answer}/n&rel=/r/PartOf&start=/c/en/{answer}&limit=5"
        graph = self.__get_concept_net_graph(CONCEPT_NET_URL_ONE)

        for edge in graph["edges"]:
            end_term = edge["end"]["term"]
            CONCEPT_NET_URL_TWO = f"http://api.conceptnet.io/query?node={end_term}&rel=/r/PartOf&end={end_term}&limit=10"
            linking_graph = self.__get_concept_net_graph(CONCEPT_NET_URL_TWO)
            for edge in linking_graph["edges"]:
                start_label = edge["start"]["label"]
                if start_label not in distractors and self.answer.lower() not in start_label.lower():
                    distractors.append(start_label)

        return distractors

    def __process_s2v_word(self, word: str) -> str:
        return word[0].split("|")[0].replace("_", " ").lower()

    def __filter_distractors(self, distractors: List[str]) -> List[str]:
        def get_edits(word):
            letters = "abcdefghijklmnopqrstuvwxyz " + string.punctuation
            splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
            deletes = [L + R[1:] for L, R in splits if R]
            transposes = [L + R[1] + R[0] + R[2:]
                          for L, R in splits if len(R) > 1]
            replaces = [L + c + R[1:] for L, R in splits if R for c in letters]
            inserts = [L + c + R for L, R in splits for c in letters]

            return set(deletes + transposes + replaces + inserts)

        edits = get_edits(self.answer.lower())
        threshold = 0.7

        filtered_distractors = [
            word for word in distractors if word.lower() not in edits]

        return [word for word in filtered_distractors if Levenshtein.normalized_distance(word.lower(), self.answer.lower()) > threshold]

    def generate_distractors_sense2vec(self, filter_output: bool = True) -> List[str]:
        answer = self.answer.lower()
        answer = answer.replace(" ", "_")

        best_sense = self.s2v.get_best_sense(answer)
        most_similar = self.s2v.most_similar(best_sense, n=20)

        distractors = [self.__process_s2v_word(
            word).title() for word in most_similar if word != self.__process_s2v_word(word)]

        distractors = list(OrderedDict.fromkeys(distractors))

        return self.__filter_distractors(distractors) if filter_output else distractors


if __name__ == "__main__":
    m = MCQEngine("ww", "USA")
    # print(m.generate_distractors_wordnet())
    # print(m.generate_distractors_conceptnet())
    print(m.generate_distractors_sense2vec())
