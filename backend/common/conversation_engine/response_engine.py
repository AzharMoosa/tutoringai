import random
from backend.common.question_engine.question_generation import retrieve_questions_by_category

uncertain_responses = ["Sorry, I did not understand the question!", 
                       "I am unable to answer that question.", 
                        "I didn't quite catch that. Please try again!"]

class ResponseEngine:
    @staticmethod
    def get_response(intents, tag: str):
        return next((random.choice(intent["responses"]) for intent in intents if intent["tag"] == tag), random.choice(uncertain_responses))

    @staticmethod
    def generate_message(message_content: str, is_answering: bool, state: dict={}):
        return {**state, "message": message_content, "isAnswering": is_answering }   
    
    @staticmethod
    def generate_answer_response(state: dict):
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
        if retrieve_questions_by_category("arithmetic")["numerical"][question_index].is_correct(int(users_answer)):
            question_index += 1
            if question_index < len(state["questionList"]):
                new_state = generate_next_question(question_index, state["questionList"])
                message = f"{random.choice(correct_response)}. Let's try another question. " + new_state["currentQuestion"]["question"]
                return ResponseEngine.generate_message(message, True, new_state)
            else:
                return ResponseEngine.generate_message(f"{random.choice(correct_response)}. That's all for now.", False)
        else:
            return ResponseEngine.generate_message(random.choice(incorrect_response), True, state)

    @staticmethod
    def generate_question_list(message_content, tag):
        question_list = retrieve_questions_by_category(tag)
        first_question = question_list["numerical"][0].question
        return {"message": f"{message_content}\n{first_question}", 
                "isAnswering": True, 
                "currentQuestion": first_question, 
                "questionList": [q.serialize() for q in question_list["numerical"]],
                "questionIndex": "0" }

    @staticmethod
    def generate_uncertain_response() -> dict:
        message = random.choice(uncertain_responses)
        return ResponseEngine.generate_message(message, is_answering=False)