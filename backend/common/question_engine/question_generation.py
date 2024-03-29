from backend.common.question_engine.question import NumericalQuestion, MultipleChoiceQuestion, TrueOrFalseQuestion
from backend.resources.db import client
import random
from bson import ObjectId
from backend.common.question_engine.graphics_question import *
from collections import defaultdict
import os

db = client["Questions"]
question_bank = list(db["question_bank"].find())

def get_numerical_questions(questions):
    return [NumericalQuestion(**question) for question in questions if question["question_type"] == "numerical"]

def get_multiple_choice_questions(questions):
    return [MultipleChoiceQuestion(**question) for question in questions if question["question_type"] == "mcq"]

def get_true_or_false_questions(questions):
    return [TrueOrFalseQuestion(**question) for question in questions if question["question_type"] == "true-or-false"]

def deserialise_questions(questions):
    deserialised = []

    for question in questions:
        if question["questionType"] == "numerical":
            deserialised.append(NumericalQuestion(**question))
        elif question["questionType"] == "mcq":
            deserialised.append(MultipleChoiceQuestion(**question))
        elif question["questionType"] == "true-or-false":
            deserialised.append(TrueOrFalseQuestion(**question))
        elif question["questionType"] == "graphical":
            if question["category"] == "trigonometry":
                deserialised.append(TriangleQuestion(**question))
            elif question["category"] == "rectangle":
                deserialised.append(RectangleQuestion(**question))
            elif question["category"] == "circle":
                deserialised.append(CircleQuestion(**question))

    return deserialised

class QuestionGenerator:
    @staticmethod
    def retrieve_one_of_each_type():
        question_sets = [question_set for question_set in question_bank]

        question_each_type = {}

        for question_set in question_sets:
            category = question_set["category"]
            if category not in question_each_type:
                question_each_type[category] = []
            question_each_type[category].append(question_set)

        return [random.choice(question_each_type[key]) for key in question_each_type.keys()]
    

    @staticmethod
    def retrieve_questions_by_category(category):
        return [question_set for question_set in question_bank if question_set["category"] == category]
    
    @staticmethod
    def __generate_question_set_by_category(t: str, room_id: str, num_questions: int = 4):
        t = t.strip()
        db = client["ChatRooms"]
        all_chatrooms = db["all_chatrooms"]

        chatroom = all_chatrooms.find_one({ "_id" : ObjectId(room_id) })

        if not chatroom:
            print("Chatroom Does Not Exist")

        if (t in chatroom["questionSetMapping"]):
            return deserialise_questions(chatroom["questionSetMapping"][t])

        question_options = QuestionGenerator.retrieve_questions_by_category(t)

        generated_questions = []

        if t == "trigonometry":
            q_options = random.choice(question_options)
            questions = q_options["questions"]
            generated_questions.extend(random.choices([TriangleQuestion(**question) for question in questions], k=2))
        elif t == "rectangle":
            q_options = random.choice(question_options)
            questions = q_options["questions"]
            generated_questions.extend(random.choices([RectangleQuestion(**question) for question in questions], k=2))
        elif t == "circle":
            q_options = random.choice(question_options)
            questions = q_options["questions"]
            generated_questions.extend(random.choices([CircleQuestion(**question) for question in questions], k=2))
        else:
            for q_options in question_options:
                questions = q_options["questions"]
                numerical_questions = get_numerical_questions(questions)

                generated_questions.extend(random.choices(numerical_questions, k=2))

                mcq_questions = get_multiple_choice_questions(questions)

                if len(mcq_questions) >= 1:
                    generated_questions.extend(random.choices(mcq_questions, k=1))

                true_or_false_questions = get_true_or_false_questions(questions)

                if len(true_or_false_questions) >= 1:
                    generated_questions.extend(random.choices(true_or_false_questions, k=1))
        
        random.shuffle(generated_questions)

        generated_questions = generated_questions[:num_questions]

        all_chatrooms.update_one({
            '_id': ObjectId(room_id)
        }, {
            '$set': {
                f"questionSetMapping.{t}": [q.serialize() for q in generated_questions]
            }
        }, upsert=False)

        return generated_questions
    
    @staticmethod
    def retrieve_assessment_mode_questions(room_id: str):
        t = "assessment"
        db = client["ChatRooms"]
        all_chatrooms = db["all_chatrooms"]

        chatroom = all_chatrooms.find_one({ "_id" : ObjectId(room_id) })

        if not chatroom:
            print("Chatroom Does Not Exist")

        if (t in chatroom["questionSetMapping"]):
            return deserialise_questions(chatroom["questionSetMapping"][t])

        question_options = QuestionGenerator.retrieve_one_of_each_type()

        questions = sum([q_options["questions"] for q_options in question_options], [])

        deserialised = []

        for question in questions:
            if question["question_type"] == "numerical":
                deserialised.append(NumericalQuestion(**question))
            elif question["question_type"] == "mcq":
                deserialised.append(MultipleChoiceQuestion(**question))
            elif question["question_type"] == "true-or-false":
                deserialised.append(TrueOrFalseQuestion(**question))
            elif question["question_type"] == "graphical":
                if question["category"] == "trigonometry":
                    deserialised.append(TriangleQuestion(**question))
                elif question["category"] == "rectangle":
                    deserialised.append(RectangleQuestion(**question))
                elif question["category"] == "circle":
                    deserialised.append(CircleQuestion(**question))

        generated_questions = []

        generated_questions.extend(random.choices([question for question in deserialised if isinstance(question, TriangleQuestion)], k=1))
        generated_questions.extend(random.choices([question for question in deserialised if isinstance(question, RectangleQuestion)], k=1))
        generated_questions.extend(random.choices([question for question in deserialised if isinstance(question, CircleQuestion)], k=1))
        generated_questions.extend(random.choices([question for question in deserialised if isinstance(question, NumericalQuestion)], k=1))

        random.shuffle(generated_questions)

        all_chatrooms.update_one({
            '_id': ObjectId(room_id)
        }, {
            '$set': {
                f"questionSetMapping.{t}": [q.serialize() for q in generated_questions]
            }
        }, upsert=False)

        return generated_questions
    
    @staticmethod
    def retrieve_question_set_by_category(t: str, room_id: str, num_questions: int = 4):
        return QuestionGenerator.__generate_question_set_by_category(t, room_id, num_questions)