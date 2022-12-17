import json

intents = json.loads(
    open("backend/common/intents/chatbot_intents.json").read())


class TestIntents:
    def test_has_intents(self):
        assert intents["intents"]
