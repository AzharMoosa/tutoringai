import random
from backend.common.question_engine.question_generation import QuestionGenerator

uncertain_responses = ["Sorry, I did not understand the question!", 
                       "I am unable to answer that question.", 
                        "I didn't quite catch that. Please try again!"]
correct_responses = ["Thats correct!"]
incorrect_responses = ["Sorry that is wrong"]

class ResponseEngine:
    @staticmethod
    def __generate_next_question(question_index, question_list):
        return {
            "currentQuestion": question_list[question_index], 
            "questionList": question_list,
            "questionIndex": str(question_index)
        }

    @staticmethod
    def get_response(intents, tag: str):
        return next((random.choice(intent["responses"]) for intent in intents if intent["tag"] == tag), random.choice(uncertain_responses))

    @staticmethod
    def generate_message(message_content: str, is_answering: bool, state: dict={}):
        return {**state, "message": message_content, "isAnswering": is_answering }
    
    @staticmethod
    def generate_uncertain_response() -> dict:
        message = random.choice(uncertain_responses)
        return ResponseEngine.generate_message(message, is_answering=False)

    @staticmethod
    def generate_incorrect_response(state):
        message = random.choice(incorrect_responses)
        return ResponseEngine.generate_message(message, is_answering=True, state=state)
    
    @staticmethod
    def generate_finish_answering_response():
        message = f"{random.choice(correct_responses)}. That's all for now."
        return ResponseEngine.generate_message(message, False)
    
    @staticmethod
    def generate_next_question_response(state, question_index):
        new_state = ResponseEngine.__generate_next_question(question_index, state["questionList"])
        message = f"{random.choice(correct_responses)}. Let's try another question. " + new_state["currentQuestion"]["question"]
        return ResponseEngine.generate_message(message, True, new_state)
    
    @staticmethod
    def generate_answer_response(state: dict):
        question_index = int(state["questionIndex"])
        users_answer = state["message"]
        question_set = QuestionGenerator.retrieve_question_set_by_category("arithmetic", state["room_id"])

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