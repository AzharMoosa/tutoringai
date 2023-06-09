import json
import os
import random

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

with open(f"{__location__}/../datasets/marc/marc-dialogue.json", 'r') as f:
    marc_dialogue_json = f.read()

marc_dialogue = json.loads(marc_dialogue_json)

class MARCDialogue:
    @staticmethod
    def get_response(tag: str):
        responses = next((response["responses"] for response in marc_dialogue if response["tag"] == tag), "As an AI Language model I am unable to answer this question.")
        return random.choice(responses)
    
    @staticmethod
    def get_uncertain_response():
        return MARCDialogue.get_response("uncertain-responses")
    
    @staticmethod
    def get_correct_response():
        return MARCDialogue.get_response("correct-responses")
    
    @staticmethod
    def get_incorrect_response():
        return MARCDialogue.get_response("incorrect-responses")
    
    @staticmethod
    def get_praise_response():
        return MARCDialogue.get_response("praise")
    
    @staticmethod
    def get_feedback_response():
        return MARCDialogue.get_response("feedback")