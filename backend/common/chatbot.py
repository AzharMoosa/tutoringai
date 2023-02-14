import random
import json
import pickle
import numpy as np
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from tensorflow.keras.models import load_model
import os
from backend.common.question_engine.question_generation import retrieve_questions

lemmatizer = WordNetLemmatizer()
__location__ = os.path.realpath(os.path.join(
    os.getcwd(), os.path.dirname(__file__)))
intents = json.loads(
    open(f"{__location__}/intents/chatbot_intents.json").read())["intents"]
words = pickle.load(open(f"{__location__}/model/words.pkl", "rb"))
classes = pickle.load(open(f"{__location__}/model/classes.pkl", "rb"))
model = load_model(f"{__location__}/model/chatbotmodel.h5")


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
    ERROR_THRESHOLD = 0.2
    result = [(i, r) for i, r in enumerate(result) if r > ERROR_THRESHOLD]

    result.sort(key=lambda x: x[1], reverse=True)

    return [{"intent": classes[r[0]], "prob": str(r[1])} for r in result]


class Chatbot:
    @staticmethod
    def generate_message(message_content, is_answering):
        return {"message": message_content, "isAnswering": is_answering }   

    @staticmethod
    def generate_response(state):
        """
        Generates a response based on the input text.

        Arguments:
            state {dict} The input text from user.

        Returns:
            {str} The output text predicted by the chatbot.
        """

        input_text = state["message"]

        if state["isAnswering"]:
            return Chatbot.generate_message("Thats correct!", False) if retrieve_questions()[0].is_correct(
            state["message"]) else Chatbot.generate_message("Sorry that is wrong", True)

        input_text = input_text.lower().strip()
        intents_list = predict_class(input_text)
        tag = intents_list[0]["intent"]
        prob = float(intents_list[0]["prob"])
        is_question = tag == "revision-mode"

        if is_question:
            return Chatbot.generate_message(retrieve_questions()[0].question, True)

        UNCERTAIN_THRESHOLD = 0.7
        uncertain_responses = ["Sorry, I did not understand the question!",
                               "I am unable to answer that question.", "I didn't quite catch that. Please try again!"]

        if prob < UNCERTAIN_THRESHOLD:
            return random.choice(uncertain_responses)

        for intent in intents:
            if intent["tag"] == tag:
                result = random.choice(intent["responses"])
                break

        return Chatbot.generate_message(result, state["isAnswering"])

if __name__ == "__main__":
    while True:
        input_text = input("Message: ")
        print(Chatbot.generate_response(input_text))
