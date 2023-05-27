import random
from backend.common.conversation_engine.util import ConversationEngineUtil
from backend.common.conversation_engine.marc_dialogue import MARCDialogue
from backend.common.question_engine.question_generation import QuestionGenerator
from backend.common.conversation_engine.natural_language_recognition import NaturalLanguageRecognition

class ResponseEngine:
    @staticmethod
    def __generate_next_question(question_index: int, question_list: list):
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
            "questionIndex": str(question_index)
        }

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
    def generate_finish_answering_response():
        message = f"{MARCDialogue.get_correct_response()}. That's all for now."
        return ResponseEngine.generate_message(message, is_answering=False)
    
    @staticmethod
    def generate_next_question_response(state, question_index):
        new_state = ResponseEngine.__generate_next_question(question_index, state["questionList"])
        message = f"{MARCDialogue.get_correct_response()}. Let's try another question. " + new_state["currentQuestion"]["question"]
        return ResponseEngine.generate_message(message, is_answering=True, state=new_state)
    
    @staticmethod
    def generate_hint_response(state):
        return ResponseEngine.generate_message("Heres a hint", is_answering=True, state=state)
    
    @staticmethod
    def generate_solution_response(state):
        return ResponseEngine.generate_message("Heres the solution", is_answering=True, state=state)
    
    @staticmethod
    def go_to_next_question(state, question_index: int):
        question_index += 1
        
        if question_index < len(state["questionList"]):
            return ResponseEngine.generate_next_question_response(state, question_index)
        else:
            return ResponseEngine.generate_finish_answering_response()

    @staticmethod
    def generate_answer_response(state: dict):
        users_answer = ConversationEngineUtil.extract_number_from_text(state["message"])

        if not users_answer:
            # User Requires Hint/Solution
            tag, prob = NaturalLanguageRecognition.predict_intention(state["message"])

            if (tag in ("solution", "hint") and prob >= ConversationEngineUtil.UNCERTAIN_THRESHOLD):
                if (tag == "hint"):
                    return ResponseEngine.generate_hint_response(state)
                else:
                    return ResponseEngine.generate_solution_response(state)
                
            return ResponseEngine.generate_incorrect_response(state) 

        # User Is Attempting To Answer
        question_index = int(state["questionIndex"])
        question_set = QuestionGenerator.retrieve_question_set_by_category(state["currentQuestion"]["category"], state["room_id"])

        if not question_set[question_index].is_correct(users_answer):
            return ResponseEngine.generate_incorrect_response(state)
        
        return ResponseEngine.go_to_next_question(state, question_index)

    @staticmethod
    def generate_question_list(message_content, tag, room_id, assessment_mode=False):
        if assessment_mode:
            question_list = QuestionGenerator.retrieve_question_set_by_category("rectangle", room_id) + QuestionGenerator.retrieve_question_set_by_category("circle", room_id)
            first_question = question_list[0]
            return {"message": f"{message_content}\n{first_question}", 
                    "isAnswering": True, 
                    "currentQuestion": first_question.serialize(), 
                    "questionList": [q.serialize() for q in question_list],
                    "questionIndex": "0" }
        else:
            question_list = QuestionGenerator.retrieve_question_set_by_category(tag, room_id)
            first_question = question_list[0]
            return {"message": f"{message_content}\n{first_question}", 
                    "isAnswering": True, 
                    "currentQuestion": first_question.serialize(), 
                    "questionList": [q.serialize() for q in question_list],
                    "questionIndex": "0" }