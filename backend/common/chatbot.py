from backend.common.conversation_engine.response_engine import ResponseEngine
from backend.common.conversation_engine.util import ConversationEngineUtil
from backend.common.conversation_engine.natural_language_recognition import NaturalLanguageRecognition

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

        if state["isAnswering"]:
            return ResponseEngine.generate_answer_response(state)
        
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

        # Solve Shape
        if tag in shape_solve:
            return ResponseEngine.generate_shape_solution(state, tag)

        return ResponseEngine.generate_message(response, state["isAnswering"])