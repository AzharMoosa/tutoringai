import os
from dotenv import load_dotenv
import requests
load_dotenv()

URL = "https://api-inference.huggingface.co/models/humarin/chatgpt_paraphraser_on_T5_base"
HEADERS = { "Authorization": f"Bearer {os.getenv('HUGGING_FACE_TOKEN')}"}

class ParaphraseModel:
    @staticmethod
    def query(input: str) -> str:
        payload = { "inputs": input, "wait_for_model": True }

        response = requests.post(URL, headers=HEADERS, json=payload).json()

        # If Error Retry Again
        if "error" in response:
            response = requests.post(URL, headers=HEADERS, json=payload).json()
            if "error" in response:
                return input

        if not response or len(response) == 0 or "generated_text" not in response[0]: 
            return input

        return response[0]["generated_text"]