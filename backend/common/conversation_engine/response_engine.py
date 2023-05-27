import random
from backend.common.conversation_engine.marc_dialogue import MARCDialogue
from backend.common.question_engine.question_generation import QuestionGenerator

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
        return ResponseEngine.generate_message(message, False)
    
    @staticmethod
    def generate_next_question_response(state, question_index):
        new_state = ResponseEngine.__generate_next_question(question_index, state["questionList"])
        message = f"{MARCDialogue.get_correct_response()}. Let's try another question. " + new_state["currentQuestion"]["question"]
        return ResponseEngine.generate_message(message, True, new_state)
    
    @staticmethod
    def generate_answer_response(state: dict):
        question_index = int(state["questionIndex"])
        users_answer = state["message"]
        question_set = QuestionGenerator.retrieve_question_set_by_category(state["currentQuestion"]["category"], state["room_id"])

        if not question_set[question_index].is_correct(users_answer):
            return ResponseEngine.generate_incorrect_response(state)
        
        question_index += 1
        
        if question_index < len(state["questionList"]):
            return ResponseEngine.generate_next_question_response(state, question_index)
        else:
            return ResponseEngine.generate_finish_answering_response()

    @staticmethod
    def generate_question_list(message_content, tag, room_id):
        question_list = QuestionGenerator.retrieve_question_set_by_category(tag, room_id)
        first_question = question_list[0]
        return {"message": f"{message_content}\n{first_question}", 
                "isAnswering": True, 
                "currentQuestion": first_question.serialize(), 
                "questionList": [q.serialize() for q in question_list],
                "questionIndex": "0" }