import random
import json
import pickle
import numpy as np
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from tensorflow.keras.models import load_model
from util import load_intent


class Chatbot:
    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()
        self.intents = load_intent()["intents"]
        self.words = pickle.load(open("words.pkl", "rb"))
        self.classes = pickle.load(open("classes.pkl", "rb"))
        self.model = load_model("chatbotmodel.h5")

    def generate_response(self, input_text):
        """
        Generates a response based on the input text.

        Arguments:
            input_text {str} The input text from user.

        Returns:
            {str} The output text predicted by the chatbot.
        """
        input_text = input_text.lower().strip()
        intents_list = self._predict_class(input_text)
        tag = intents_list[0]["intent"]
        for intent in self.intents:
            if intent["tag"] == tag:
                result = random.choice(intent["responses"])
                break
        return result

    def _parse_text(self, text):
        """
        Returns a list of lemmatized words based on the input text.

        Arguments:
            text {str} The input text from user.

        Returns:
            {list} A list of lemmatized words.
        """
        tokenized_words = word_tokenize(text)
        return [self.lemmatizer.lemmatize(word) for word in tokenized_words]

    def _generate_bag_of_words(self, text):
        """
        Returns bag of words using the input text

        Arguments:
            text {str} The input text from user.

        Returns:
            {np.array} - Bag of words
        """
        parsed_text = self._parse_text(text)
        bag = [0] * len(self.words)
        for w in parsed_text:
            for i, word in enumerate(self.words):
                if w == word:
                    bag[i] = 1

        return np.array(bag)

    def _predict_class(self, sentence):
        bag_of_words = self._generate_bag_of_words(sentence)
        result = self.model.predict(np.array([bag_of_words]), verbose=0)[0]
        ERROR_THRESHOLD = 0.2
        result = [(i, r) for i, r in enumerate(result) if r > ERROR_THRESHOLD]

        result.sort(key=lambda x: x[1], reverse=True)

        return [{"intent": self.classes[r[0]],
                 "prob": str(r[1])} for r in result]


if __name__ == "__main__":
    print("Running Chatbot")
    chatbot = Chatbot()

    while True:
        text = input("> ")
        if text in ("quit", "q"):
            break
        response = chatbot.generate_response(text)
        print(response)
