import random
import json
import pickle
import numpy as np
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from tensorflow.keras.models import load_model
import os
from backend.common.question_engine.question_generation import retrieve_questions_by_category

lemmatizer = WordNetLemmatizer()
__location__ = os.path.realpath(os.path.join(
    os.getcwd(), os.path.dirname(__file__)))
intents = json.loads(
    open(f"{__location__}/intents/chatbot_intents.json").read())["intents"]
words = pickle.load(open(f"{__location__}/model/words.pkl", "rb"))
classes = pickle.load(open(f"{__location__}/model/classes.pkl", "rb"))
model = load_model(f"{__location__}/model/chatbotmodel.h5")
topics = ["arithmetic"]

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

    if not result:
        return []

    result.sort(key=lambda x: x[1], reverse=True)

    return [{"intent": classes[r[0]], "prob": str(r[1])} for r in result]


class Chatbot:
    @staticmethod
    def generate_answer_response(state):
        def generate_next_question(question_index, question_list):
            return {
                "currentQuestion": question_list[question_index], 
                "questionList": question_list,
                "questionIndex": str(question_index)
            }

        question_index = int(state["questionIndex"])
        users_answer = state["message"]
        correct_response = ["Thats correct!"]
        incorrect_response = ["Sorry that is wrong"]
        if retrieve_questions_by_category("arithmetic")[question_index].is_correct(users_answer):
            question_index += 1
            if question_index < len(state["questionList"]):
                new_state = generate_next_question(question_index, state["questionList"])
                message = f"{random.choice(correct_response)}. " + new_state["currentQuestion"]["question"]
                return Chatbot.generate_message(message, True, new_state)
            else:
                return Chatbot.generate_message(random.choice(correct_response), False)
        else:
            return Chatbot.generate_message(random.choice(incorrect_response), True, state)

    @staticmethod
    def generate_question_list(message_content, tag):
        question_list = retrieve_questions_by_category(tag)
        first_question = question_list[0].question
        return {"message": f"{message_content}\n{first_question}", 
                "isAnswering": True, 
                "currentQuestion": first_question, 
                "questionList": [q.serialize() for q in question_list],
                "questionIndex": "0" }

    @staticmethod
    def generate_message(message_content, is_answering, state={}):
        return {**state, "message": message_content, "isAnswering": is_answering }   

    @staticmethod
    def generate_response(state):
        """
        Generates a response based on the input text.

        Arguments:
            state {dict} The input text from user.

        Returns:
            {str} The output text predicted by the chatbot.
        """
        state["message"] = state["message"].lower().strip()
        input_text = state["message"]

        intents_list = predict_class(input_text)
        tag = intents_list[0]["intent"]
        prob = float(intents_list[0]["prob"])

        if state["isAnswering"]:
            return Chatbot.generate_answer_response(state)

        UNCERTAIN_THRESHOLD = 0.4
        uncertain_responses = ["Sorry, I did not understand the question!",
                               "I am unable to answer that question.", "I didn't quite catch that. Please try again!"]

        if prob < UNCERTAIN_THRESHOLD:
            return Chatbot.generate_message(random.choice(uncertain_responses), False)

        result = next((random.choice(intent["responses"]) for intent in intents if intent["tag"] == tag), random.choice(uncertain_responses))

        if tag in topics:
            return Chatbot.generate_question_list(result, tag)

        return Chatbot.generate_message(result, state["isAnswering"])