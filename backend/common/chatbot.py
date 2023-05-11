import random
import json
import pickle
import numpy as np
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from tensorflow.keras.models import load_model
import os
from backend.common.conversation_engine.response_engine import ResponseEngine
from collections import defaultdict

lemmatizer = WordNetLemmatizer()
__location__ = os.path.realpath(os.path.join(
    os.getcwd(), os.path.dirname(__file__)))

def merge_intents(*args):
    m = defaultdict(list)
    for d in args:
        for k, v in d.items():
            if isinstance(v, list):
                m[k].extend(v)
            else:
                m[k].append(v)
    return dict(m)

def load_intent():
    marc_intent = json.loads(open(f"{__location__}/intents/chatbot_intents.json").read())
    prosocial_intent = json.loads(open(f"{__location__}/datasets/prosocial/prosocial_intent.json").read())
    return merge_intents(marc_intent, prosocial_intent)

intents = load_intent()["intents"]
words = pickle.load(open(f"{__location__}/model/words.pkl", "rb"))
classes = pickle.load(open(f"{__location__}/model/classes.pkl", "rb"))
model = load_model(f"{__location__}/model/chatbotmodel.h5")
topics = ["arithmetic", "trigonometry", "rectangle", "circle"]
UNCERTAIN_THRESHOLD = 0.4

def parse_text(text):
    """
    Returns a list of lemmatized words based on the input text.

    Arguments:
        text {str} The input text from user.

    Returns:
        {list} A list of lemmatized words.
    """
    tokenized_words = word_tokenize(text)
    return [lemmatizer.lemmatize(word) for word in tokenized_words]


def generate_bag_of_words(text):
    """
    Returns bag of words using the input text

    Arguments:
        text {str} The input text from user.

    Returns:
        {np.array} - Bag of words
    """
    parsed_text = parse_text(text)
    bag = [0] * len(words)
    for w in parsed_text:
        for i, word in enumerate(words):
            if w == word:
                bag[i] = 1

    return np.array(bag)


def predict_class(sentence):
    bag_of_words = generate_bag_of_words(sentence)
    result = model.predict(np.array([bag_of_words]), verbose=0)[0]
    ERROR_THRESHOLD = 0.4
    result = [(i, r) for i, r in enumerate(result) if r > ERROR_THRESHOLD]

    if not result:
        return []

    result.sort(key=lambda x: x[1], reverse=True)

    return [{"intent": classes[r[0]], "prob": str(r[1])} for r in result]


class Chatbot:
    @staticmethod
    def generate_response(state: dict):
        """
        Generates a response based on the input text.

        Arguments:
            state {dict} The input state from user.

        Returns:
            {dict} The output state.
        """
        state["message"] = state["message"].lower().strip()
        input_text = state["message"]

        if state["isAnswering"]:
            return ResponseEngine.generate_answer_response(state)
        
        intents_list = predict_class(input_text)
        tag = intents_list[0]["intent"] if len(intents_list) > 0 else None
        prob = float(intents_list[0]["prob"]) if len(intents_list) > 0 else 0.0
        
        if prob < UNCERTAIN_THRESHOLD:
            return ResponseEngine.generate_uncertain_response()

        response = ResponseEngine.get_response(intents, tag)

        if tag in topics:
            return ResponseEngine.generate_question_list(response, tag, state["room_id"])

        return ResponseEngine.generate_message(response, state["isAnswering"])