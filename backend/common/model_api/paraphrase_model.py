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

        return response[0]["generated_text"] if response else ""