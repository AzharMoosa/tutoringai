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
        """
        Performs post processing on the input text and
        returns the processed text.

        Arguments:
            text {str} The input text to be processed

        Returns:
            {str} The processed text
        """
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
        """
        The input text is first preprocessed and encoded
        using the tokenizer. Then the input ids and 
        attention mask is extracted.

        Arguments:
            text {str} The input text to be encoded

        Returns:
            {tuple()} The input ids and the attention mask
        """
        text = TextSummarization.__preprocess_text(text)
        max_length = 512
        encoder = tokenizer.encode_plus(text, 
                                        max_length=max_length, 
                                        pad_to_max_length=False, 
                                        truncation=True, 
                                        return_tensors="pt").to(device)

        return encoder["input_ids"], encoder["attention_mask"]
    
    @staticmethod
    def summarize(text: str, min_length=75, max_length=300) -> str:
        """
        Performs text summarization on the input text. First the
        input ids and attention mask is retreived. Then the T5
        model is used to generated a summarized text. The model
        output is then decoded and processed to retreive the
        summarized text.

        Arguments:
            text {str} The input text to be summarized.

        Returns:
            {str} The summarized text
        """
        input_ids, attention_mask = TextSummarization.__get_input_ids_attention_mask(text)

        model_output = model.generate(input_ids=input_ids,
                                      attention_mask=attention_mask,
                                      early_stopping=True,
                                      num_beams=3,
                                      num_return_sequences=1,
                                      no_repeat_ngram_size=2,
                                      min_length=min_length,
                                      max_length=max_length)
        
        decoded_output = [tokenizer.decode(id, skip_special_tokens=True) for id in model_output]
        
        return TextSummarization.__postprocess_text(decoded_output[0]).strip()

if __name__ == "__main__":
    print(TextSummarization.summarize("John, Joe, Sarah are playing football. John has 3 apple and Joe has 2 apples. Joe gives 2 apples to John. Sarah has 9 apples. John gives 4 apples to Sarah. How many apples does John have?", min_length=50, max_length=50))