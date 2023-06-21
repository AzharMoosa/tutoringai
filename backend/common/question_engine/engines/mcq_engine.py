from nltk.corpus import wordnet
from typing import List, Tuple
import nltk
import re
import random
import json
import requests
from collections import OrderedDict
import string
from sense2vec import Sense2Vec
from rapidfuzz.distance import Levenshtein
from sentence_transformers import SentenceTransformer
from typing import List, Tuple
import itertools
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import os
nltk.download("wordnet")

model = SentenceTransformer('all-MiniLM-L12-v2')

__location__ = os.path.realpath(os.path.join(
    os.getcwd(), os.path.dirname(__file__)))

s2v = Sense2Vec().from_disk(f"{__location__}/s2v")

class MCQEngine:
    @staticmethod
    def __get_synset(word: str):
        """
        Gets the synset of a given word

        Arguments:
            word {str} The word to generate the synset from

        Returns:
            {synset} The synset from the word
        """
        return wordnet.synsets(word, "n")

    def generate_distractors_wordnet(correct_answer: str) -> List[List[str]]:
        """
        Generates the distractors using wordnet. First the synset
        of a word is retrieved. Then for each synset, the hyponyms
        are determined and added to the distractor list.

        Returns:
            {List[List[str]]} The distractors for the correct answer
        """
        distractors = []

        answer = correct_answer.lower()
        synset = MCQEngine.__get_synset(answer)
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
                if name != correct_answer.lower():
                    name = name.replace(" ", "_")
                    name = " ".join(w.capitalize() for w in name.split())
                    if name and name not in distractors:
                        distractor.append(name)

            distractors.append(distractor)

        return distractors

    @staticmethod
    def __get_concept_net_graph(url: str) -> dict:
        """
        Gets the concept net graph using the url

        Arguments:
            url {str} The API endpoint to retrieve concept net graph

        Returns:
            {dict} The concept net graph
        """
        return requests.get(url).json()

    def generate_distractors_conceptnet(correct_answer: str) -> List[str]:
        """
        Generates the distractors using conceptnet. First the
        graph is generated using the answer. Then the end term
        is used to find the connections to the answer. Finally,
        the distractors are added to the list.

        Returns:
            {List[str]} The distractors for the correct answer
        """
        distractors = []

        answer = correct_answer.lower()
        answer = answer.replace(" ", "_")
        CONCEPT_NET_URL_ONE = f"http://api.conceptnet.io/query?node=/c/en/{answer}/n&rel=/r/PartOf&start=/c/en/{answer}&limit=5"
        graph = MCQEngine.__get_concept_net_graph(CONCEPT_NET_URL_ONE)

        for edge in graph["edges"]:
            end_term = edge["end"]["term"]
            CONCEPT_NET_URL_TWO = f"http://api.conceptnet.io/query?node={end_term}&rel=/r/PartOf&end={end_term}&limit=10"
            linking_graph = MCQEngine.__get_concept_net_graph(CONCEPT_NET_URL_TWO)
            for edge in linking_graph["edges"]:
                start_label = edge["start"]["label"]
                if start_label not in distractors and correct_answer.lower() not in start_label.lower():
                    distractors.append(start_label)

        return distractors

    @staticmethod
    def __process_s2v_word(word: str) -> str:
        """
        Processes the word generated from s2v

        Arguments:
            word {str} The word to be processed

        Returns:
            {str} Processed word
        """
        return word[0].split("|")[0].replace("_", " ").lower()

    @staticmethod
    def __filter_distractors_edit_distance(correct_answer: str, distractors: List[str]) -> List[str]:
        """
        Filters the distractors using Levenshtein Normalized Distance

        Arguments:
            distractors {List[str]} The distractors to be filtered

        Returns:
            {List[str]} The filtered distractors
        """
        def get_edits(word):
            letters = "abcdefghijklmnopqrstuvwxyz " + string.punctuation
            splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
            deletes = [L + R[1:] for L, R in splits if R]
            transposes = [L + R[1] + R[0] + R[2:]
                          for L, R in splits if len(R) > 1]
            replaces = [L + c + R[1:] for L, R in splits if R for c in letters]
            inserts = [L + c + R for L, R in splits for c in letters]

            return set(deletes + transposes + replaces + inserts)

        edits = get_edits(correct_answer.lower())
        threshold = 0.7

        filtered_distractors = [
            word for word in distractors if word.lower() not in edits]

        return [word for word in filtered_distractors if Levenshtein.normalized_distance(word.lower(), correct_answer.lower()) > threshold]

    @staticmethod
    def generate_distractors_sense2vec(correct_answer: str, filter_output: bool = True) -> List[str]:
        """
        Generates the distractors using sense2vec. First the best
        sense is determined. Then the most similar words are found.

        Arguments:
            filter_output {bool} The flag to determine if the output
                                 should be filtered using edit
                                 distance

        Returns:
            {List[str]} The distractors for the correct answer
        """
        answer = correct_answer.lower()
        answer = answer.replace(" ", "_")

        best_sense = s2v.get_best_sense(answer)
        if not best_sense:
            return []
        
        most_similar = s2v.most_similar(best_sense, n=20)

        distractors = [MCQEngine.__process_s2v_word(
            word).title() for word in most_similar if word != MCQEngine.__process_s2v_word(word)]

        distractors = list(OrderedDict.fromkeys(distractors))

        return MCQEngine.__filter_distractors_edit_distance(correct_answer, distractors) if filter_output else distractors

    @staticmethod
    def filter_distractors_mmr(document_embeddings: np.ndarray, word_embeddings: np.ndarray, distractors: List[str], top_n=5, diversity: float = 0.9) -> List[Tuple[str, float]]:
        """
        Adapted from https://github.com/MaartenGr/KeyBERT/blob/master/keybert/_mmr.py
        @author - Maarten Grootendorst,
        @title - KeyBERT: Minimal keyword extraction with BERT
        @year - 2020,
        @publisher - Zenodo
        @version - v0.3.0
        @doi - 10.5281/zenodo.4461265
        @url - https://doi.org/10.5281/zenodo.4461265
        """
        similarity = cosine_similarity(word_embeddings, document_embeddings)
        word_similarity = cosine_similarity(word_embeddings)

        keyword_idx = [np.argmax(similarity)]
        candidates_idx = [i for i in range(
            len(distractors)) if i != keyword_idx[0]]

        for _ in range(top_n - 1):
            c_similarities = similarity[candidates_idx, :]
            t_similarities = np.max(
                word_similarity[candidates_idx][:, keyword_idx], axis=1)
            mmr = (1 - diversity) * c_similarities - \
                diversity * t_similarities.reshape(-1, 1)
            mmr_idx = candidates_idx[np.argmax(mmr)]

            keyword_idx.append(mmr_idx)
            candidates_idx.remove(mmr_idx)

        return [(distractors[idx], round(float(similarity.reshape(1, -1)[0][idx]), 4)) for idx in keyword_idx]

    @staticmethod
    def __get_embeddings(correct_answer: str, distractors: List[str]) -> Tuple[np.ndarray, np.ndarray]:
        """
        Generates the answer and document embeddings

        Arguments:
            distractors {List[str]} The list of distractors

        Returns:
            {Tuple[np.ndarry, np.ndarray]} The answer and document embeddings
        """
        return model.encode([correct_answer]), model.encode(distractors)

    def generate_distractors_transformer(correct_answer: str) -> List[str]:
        """
        Generates the distractors using sentence transformers. The
        distractors are generated using sense2vec. Then it is filtered
        using MMR to determine the correct distractors.

        Returns:
            {List[str]} The distractors for the correct answer
        """
        s2v_distractors = MCQEngine.generate_distractors_sense2vec(correct_answer)
        distractors = [correct_answer] + s2v_distractors
        try:
            a_embedding, d_embedding = MCQEngine.__get_embeddings(correct_answer, distractors)
            filtered_distractors = MCQEngine.filter_distractors_mmr(
                a_embedding, d_embedding, distractors)
            return [distractor[0] for distractor in filtered_distractors][1:]
        except:
            return s2v_distractors