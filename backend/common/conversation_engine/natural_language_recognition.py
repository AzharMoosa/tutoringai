import pickle
import numpy as np
import nltk
nltk.download('punkt')
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from tensorflow.keras.models import load_model
from typing import Tuple
import os

lemmatizer = WordNetLemmatizer()
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

words = pickle.load(open(f"{__location__}/../model/words.pkl", "rb"))
classes = pickle.load(open(f"{__location__}/../model/classes.pkl", "rb"))
model = load_model(f"{__location__}/../model/chatbotmodel.h5")
topics = ["arithmetic", "trigonometry", "rectangle", "circle"]

class NaturalLanguageRecognition:
    @staticmethod
    def __parse_text(text):
        """
        Returns a list of lemmatized words based on the input text.

        Arguments:
            text {str} The input text from user.

        Returns:
            {list} A list of lemmatized words.
        """
        tokenized_words = word_tokenize(text)
        return [lemmatizer.lemmatize(word) for word in tokenized_words]

    @staticmethod
    def __generate_bag_of_words(text):
        """
        Returns bag of words using the input text

        Arguments:
            text {str} The input text from user.

        Returns:
            {np.array} - Bag of words
        """
        parsed_text = NaturalLanguageRecognition.__parse_text(text)
        bag = [0] * len(words)
        for w in parsed_text:
            for i, word in enumerate(words):
                if w == word:
                    bag[i] = 1

        return np.array(bag)

    @staticmethod
    def __predict_class(sentence):
        bag_of_words = NaturalLanguageRecognition.__generate_bag_of_words(sentence)
        result = model.predict(np.array([bag_of_words]), verbose=0)[0]
        ERROR_THRESHOLD = 0.4
        result = [(i, r) for i, r in enumerate(result) if r > ERROR_THRESHOLD]

        if not result:
            return []

        result.sort(key=lambda x: x[1], reverse=True)

        return [{"intent": classes[r[0]], "prob": str(r[1])} for r in result]
    
    @staticmethod
    def predict_intention(text: str) -> Tuple[str, float]:
        intents_list = NaturalLanguageRecognition.__predict_class(text)
        tag = intents_list[0]["intent"] if len(intents_list) > 0 else None
        prob = float(intents_list[0]["prob"]) if len(intents_list) > 0 else 0.0
        return tag, prob
    