from backend.common.conversation_engine.response_engine import ResponseEngine
from backend.common.conversation_engine.util import ConversationEngineUtil
from backend.common.conversation_engine.natural_language_recognition import NaturalLanguageRecognition
import re
import traceback

intents = ConversationEngineUtil.load_intent()["intents"]
topics = ["arithmetic", "trigonometry", "rectangle", "circle"]
shape_solve = ["triangle-area", "rectangle-area", "circle-area", "circle-circumference"]

class Chatbot:
    @staticmethod
    def generate_response(state: dict):
        """
        Generates a response based on the input text.

        Arguments:
            state {dict} The input state from user.

        Returns:
            {dict} The output state.
        """
        state["message"] = state["message"].lower().strip()
        input_text = state["message"]

        try:
            if state["isAnswering"]:
                return ResponseEngine.generate_answer_response(state)
            
            ARITHMETIC_SIMPLE_PATTERN =  r"^\b\d+\s*[-+*/]\s*\d+\b$"

            if re.match(ARITHMETIC_SIMPLE_PATTERN, input_text) or ResponseEngine.contains_arithmetic_equations(input_text):
                return ResponseEngine.generate_simple_arithmetic_solution(state) 
            
            tag, prob = NaturalLanguageRecognition.predict_intention(input_text)
            
            if prob < ConversationEngineUtil.UNCERTAIN_THRESHOLD or tag in ConversationEngineUtil.ANSWERING_MODE_ONLY_TAGS:
                return ResponseEngine.generate_uncertain_response()

            response = ResponseEngine.get_response(intents, tag)

            # Revision Mode
            if tag in topics:
                return ResponseEngine.generate_question_list(response, tag, state["room_id"])
            
            # Assessment Mode
            if tag == "assessment-mode":
                return ResponseEngine.generate_question_list(response, tag, state["room_id"], assessment_mode=True)

            # Solve Shape Question
            if tag in shape_solve:
                return ResponseEngine.generate_shape_solution(state, tag)
            
            # Solve Worded Question
            if tag == "solve":
                return ResponseEngine.generate_worded_problem_solution(state, tag)

            return ResponseEngine.generate_message(response, state["isAnswering"])
        except:
            traceback.print_exc()
            return ResponseEngine.generate_message("Sorry! As a language model, I am unable to answer this!", state["isAnswering"])