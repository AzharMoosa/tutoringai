import re
import json
import os
from collections import defaultdict

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

class ConversationEngineUtil:
    UNCERTAIN_THRESHOLD = 0.6
    ANSWERING_MODE_ONLY_TAGS = ["hint", "answer", "solution"]

    @staticmethod
    def extract_number_from_text(text: str) -> float:
        numbers = re.findall(r"\d+\.\d+|\d+", text)
        return float(numbers[-1]) if numbers else None
    
    @staticmethod
    def merge_intents(*args):
        m = defaultdict(list)
        for d in args:
            for k, v in d.items():
                if isinstance(v, list):
                    m[k].extend(v)
                else:
                    m[k].append(v)
        return dict(m)
    
    @staticmethod
    def load_intent():
        marc_intent = json.loads(open(f"{__location__}/../intents/chatbot_intents.json").read())
        return ConversationEngineUtil.merge_intents(marc_intent)