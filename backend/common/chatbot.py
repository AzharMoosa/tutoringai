from backend.common.conversation_engine.response_engine import ResponseEngine
from backend.common.conversation_engine.util import ConversationEngineUtil
from backend.common.conversation_engine.natural_language_recognition import NaturalLanguageRecognition

intents = ConversationEngineUtil.load_intent()["intents"]
topics = ["arithmetic", "trigonometry", "rectangle", "circle"]

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
        
        if tag == "assessment-mode":
            return ResponseEngine.generate_question_list(response, tag, state["room_id"], assessment_mode=True)

        return ResponseEngine.generate_message(response, state["isAnswering"])