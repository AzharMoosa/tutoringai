from nltk.corpus import wordnet
from typing import List
import nltk
import re
import random
import json
import requests
nltk.download("wordnet")


class MCQEngine:
    def __init__(self, question: str, answer: str) -> None:
        self.question = question
        self.answer = answer

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


if __name__ == "__main__":
    m = MCQEngine("ww", "California")
    # print(m.generate_distractors_wordnet())
    print(m.generate_distractors_conceptnet())
