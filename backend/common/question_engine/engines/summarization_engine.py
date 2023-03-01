import torch
from transformers import T5ForConditionalGeneration, T5Tokenizer
import random
import numpy as np
import nltk
nltk.download("punkt")
nltk.download("brown")
nltk.download("wordnet")
from nltk.corpus import wordnet
from nltk.tokenize import sent_tokenize

model = T5ForConditionalGeneration.from_pretrained("t5-base")
tokenizer = T5Tokenizer.from_pretrained("t5-base")

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Device {device}")
model = model.to(device)

class TextSummarization:
    @staticmethod
    def __postprocess_text(text: str) -> str:
        processed_text = ""
        sentences = sent_tokenize(text)

        for sentence in sentences:
            processed_text += " " + sentence.capitalize()

        return processed_text
    
    @staticmethod
    def __preprocess_text(text: str) -> str:
        text = text.strip().replace("\n", " ")
        return "summarize: " + text
    
    @staticmethod
    def __get_input_ids_attention_mask(text: str):
        text = TextSummarization.__preprocess_text(text)
        max_length = 512
        encoder = tokenizer.encode_plus(text, 
                                        max_length=max_length, 
                                        pad_to_max_length=False, 
                                        truncation=True, 
                                        return_tensors="pt").to(device)

        return encoder["input_ids"], encoder["attention_mask"]
    
    @staticmethod
    def summarize(text) -> str:
        input_ids, attention_mask = TextSummarization.__get_input_ids_attention_mask(text)

        model_output = model.generate(input_ids=input_ids,
                                      attention_mask=attention_mask,
                                      early_stopping=True,
                                      num_beams=3,
                                      num_return_sequences=1,
                                      no_repeat_ngram_size=2,
                                      min_length=75,
                                      max_length=300)
        
        decoded_output = [tokenizer.decode(id, skip_special_tokens=True) for id in model_output]
        
        return TextSummarization.__postprocess_text(decoded_output[0]).strip()

if __name__ == "__main__":
    print(TextSummarization.summarize("A Lion lay asleep in the forest, his great head resting on his paws. A timid little Mouse came upon him unexpectedly, and in her fright and haste to get away, ran across the Lion's nose. Roused from his nap, the Lion laid his huge paw angrily on the tiny creature to kill her.  \"Spare me!\" begged the poor Mouse. \"Please let me go and some day I will surely repay you.\"  The Lion was much amused to think that a Mouse could ever help him. But he was generous and finally let the Mouse go.  Some days later, while stalking his prey in the forest, the Lion was caught in the toils of a hunter's net. Unable to free himself, he filled the forest with his angry roaring. The Mouse knew the voice and quickly found the Lion struggling in the net. Running to one of the great ropes that bound him, she gnawed it until it parted, and soon the Lion was free. \"You laughed when I said I would repay you,\" said the Mouse. \"Now you see that even a Mouse can help a Lion."))