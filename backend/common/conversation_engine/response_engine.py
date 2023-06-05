import random
from backend.common.conversation_engine.util import ConversationEngineUtil
from backend.common.conversation_engine.marc_dialogue import MARCDialogue
from backend.common.question_engine.question_generation import QuestionGenerator
from backend.common.conversation_engine.natural_language_recognition import NaturalLanguageRecognition
from backend.common.tutoring_engine.tutoring_engine import TutoringEngine
from backend.common.tutoring_engine.shape_solver import ShapeQuestionSolver
from bson import ObjectId
from backend.resources.db import client
import traceback

ASSESSMENT_MODE = "assessment"
REVISION_MODE = "revision"

class ResponseEngine:
    @staticmethod
    def __generate_next_question(question_index: int, question_list: list, correct_answers: int):
        """
        Returns the next question from the question list

        Arguments:
            question_index {int} The current question that user is on
            question_list  {list} A list of questions to choose from

        Returns:
            {dict} - Updated Question State
        """
        return {
            "currentQuestion": question_list[question_index], 
            "questionList": question_list,
            "questionIndex": str(question_index),
            "correctAnswers": str(correct_answers)
        }
    
    @staticmethod
    def update_recent_topic(user_id, mode, total_answered, topic="-", correctly_answered="0"):
        try:
            db = client["Users"]
            all_users = db.all_users
            user = all_users.find_one({ "_id" : ObjectId(user_id) })

            # Verify User Exists
            if not user:
                return {"error": "User Does Not Exist!"}, 403
            
            recentTopics = user["recentTopics"] if "recentTopics" in user else []

            if mode == ASSESSMENT_MODE:
                recentTopic = { "mode": mode, "totalAnswered": total_answered, "correctlyAnswered": correctly_answered }
            else:
                recentTopic = { "topic": topic, "mode": mode, "totalAnswered": total_answered }

            recentTopics.insert(0, recentTopic)

            # Update User
            all_users.update_one({
                '_id': user["_id"]
            }, {
                '$set': {
                    'recentTopics': recentTopics
                }
            }, upsert=False)

        except Exception:
            traceback.print_exc()
            return {'error': "Server Error! Unable to update user, please try again."}, 500

    @staticmethod
    def get_response(intents, tag: str):
        return next((random.choice(intent["responses"]) for intent in intents if intent["tag"] == tag), MARCDialogue.get_uncertain_response())

    @staticmethod
    def generate_message(message_content: str, is_answering: bool, state: dict={}):
        return {**state, "message": message_content, "isAnswering": is_answering }
    
    @staticmethod
    def generate_uncertain_response() -> dict:
        message = MARCDialogue.get_uncertain_response()
        return ResponseEngine.generate_message(message, is_answering=False)

    @staticmethod
    def generate_incorrect_response(state):
        message = MARCDialogue.get_incorrect_response()
        return ResponseEngine.generate_message(message, is_answering=True, state=state)
    
    @staticmethod
    def generate_finish_answering_response(state, correct_answers):
        if state["mode"] == ASSESSMENT_MODE:
            message = "That's all for now."
        else:
            message = f"{MARCDialogue.get_correct_response()}. That's all for now."
        ResponseEngine.update_recent_topic(state["room_id"], 
                                           state["mode"], 
                                           len(state["questionList"]), 
                                           topic=state["currentQuestion"]["category"], 
                                           correctly_answered=correct_answers)
        return ResponseEngine.generate_message(message, is_answering=False)
    
    @staticmethod
    def generate_next_question_response(state, question_index, correct_answers):
        new_state = ResponseEngine.__generate_next_question(question_index, state["questionList"], correct_answers)
        if state["mode"] == ASSESSMENT_MODE:
            message = new_state["currentQuestion"]["question"]
        else:
            message = f"{MARCDialogue.get_correct_response()}. Let's try another question. " + new_state["currentQuestion"]["question"]
        return ResponseEngine.generate_message(message, is_answering=True, state=new_state)
    
    @staticmethod
    def generate_hint_response(state):
        return ResponseEngine.generate_message("Heres a hint", is_answering=True, state=state)
    
    @staticmethod
    def generate_shape_solution(state, tag):
        solution = ShapeQuestionSolver.parse_shape_question(state["message"], tag)
        return ResponseEngine.generate_message(solution, state["isAnswering"])

    @staticmethod
    def generate_worded_problem_solution(state, tag):
        solution = "worded_problem"
        return ResponseEngine.generate_message(solution, state["isAnswering"])
    
    @staticmethod
    def contains_arithmetic_equations(text):
        return TutoringEngine.contains_simple_arithmetics(text) 
    
    @staticmethod
    def generate_simple_arithmetic_solution(state):
        solution = TutoringEngine.solve_simple_arithmetics(state["message"])
        return ResponseEngine.generate_message(solution, state["isAnswering"]) 
    
    @staticmethod
    def go_to_next_question(state, question_index: int, correct_answers: int):
        question_index += 1
        
        if question_index < len(state["questionList"]):
            return ResponseEngine.generate_next_question_response(state, question_index, correct_answers)
        else:
            return ResponseEngine.generate_finish_answering_response(state, correct_answers)

    @staticmethod
    def generate_answer_response(state: dict):
        users_answer = state["message"]
        question_index = int(state["questionIndex"])
        correct_answers = int(state["correctAnswers"])
        question_set = QuestionGenerator.retrieve_question_set_by_category(state["currentQuestion"]["category"], state["room_id"])
        current_question = question_set[question_index]

        # User Requires Hint/Solution
        tag, prob = NaturalLanguageRecognition.predict_intention(users_answer)

        if (tag in ("solution", "hint") and prob >= ConversationEngineUtil.UNCERTAIN_THRESHOLD):
            if state["mode"] == ASSESSMENT_MODE:
                return ResponseEngine.generate_message("Unfortunately, I cannot give you a assist during this assessment. However, I will help you once we have completed this assessment", is_answering=True, state=state)

            if (tag == "hint"):
                return ResponseEngine.generate_hint_response(state)
            else:
                solution = TutoringEngine.solve_question(current_question)
                return ResponseEngine.generate_message(solution, is_answering=True, state=state)
                
        # User Is Attempting To Answer
        if not current_question.is_correct(users_answer):
            if state["mode"] == ASSESSMENT_MODE:
                return ResponseEngine.go_to_next_question(state, question_index, correct_answers)
            else:
                return ResponseEngine.generate_incorrect_response(state)
        
        if state["mode"] == ASSESSMENT_MODE:
            correct_answers += 1
        
        return ResponseEngine.go_to_next_question(state, question_index, correct_answers)

    @staticmethod
    def generate_question_list(message_content, tag, room_id, assessment_mode=False):
        if assessment_mode:
            # TODO: Get Assessment Questions
            question_list = QuestionGenerator.retrieve_question_set_by_category("rectangle", room_id)
            first_question = question_list[0]
            return {"message": f"{message_content}\n{first_question}", 
                    "isAnswering": True, 
                    "currentQuestion": first_question.serialize(), 
                    "questionList": [q.serialize() for q in question_list],
                    "questionIndex": "0",
                    "mode": ASSESSMENT_MODE,
                    "correctAnswers": "0" }
        else:
            question_list = QuestionGenerator.retrieve_question_set_by_category(tag, room_id)
            first_question = question_list[0]
            return {"message": f"{message_content}\n{first_question}", 
                    "isAnswering": True, 
                    "currentQuestion": first_question.serialize(), 
                    "questionList": [q.serialize() for q in question_list],
                    "questionIndex": "0",
                    "mode": REVISION_MODE,
                    "correctAnswers": "0" }