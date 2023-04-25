import os
from dotenv import load_dotenv
import requests
from requests import Response
import json
from nltk import tokenize
load_dotenv()

GPT_URL = "https://api-inference.huggingface.co/models/EleutherAI/gpt-j-6b"
HUGGING_FACE_TOKEN = { "Authorization": f"Bearer {os.getenv('HUGGING_FACE_TOKEN')}"}

class MathGPT:
    @staticmethod
    def __get_gpt_response(input: str):
        payload = {
            "inputs":input,
            "parameters":  {
                "return_full_text": False,
                "use_cache": True,
                "max_new_tokens": 25
            }
        }

        data = json.dumps(payload)
        return requests.request("POST", GPT_URL, headers=HUGGING_FACE_TOKEN, data=data)
    
    @staticmethod
    def __decode_gpt_response(response: Response) -> str:
        data = json.loads(response.content.decode("utf-8"))
        if len(data) == 0:
            return "Sorry! I am unable to answer that question!"
        return data[0]["generated_text"]
    
    @staticmethod
    def __parse_gpt_response(text: str) -> str:
        tokens = text.split("Human:")
        if len(tokens) == 0:
            return "Sorry! I am unable to answer that question!"
        return str(tokens[0]).strip("\n").strip()
    
    @staticmethod
    def send_query(input: str) -> list:
        # Get Generated Text Using GPT
        response = MathGPT.__get_gpt_response(f"Human: {input} Bot:")
        text = MathGPT.__decode_gpt_response(response)
        return MathGPT.__parse_gpt_response(text)
    
if __name__ == "__main__":
    result = MathGPT.send_query("John, Joe, Sarah are in the park playing football and enjoying the sunny weather. They stop to have some lunch. John has 3 apples in his lunchbox. Joe has 2 apples in his lunchbox. Joe is feeling generous and gives 2 apples to John. Sarah also has 9 apples in her lunchbox. John is full and gives 4 apples to Sarah. How many apples does John now have?")
    print(result)