import names
import re
from typing import List
import random
from keyword_extraction_engine import KeywordExtraction
from mcq_engine import MCQEngine
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
model_name = "humarin/chatgpt_paraphraser_on_T5_base"
device = 'cuda' if torch.cuda.is_available() else 'cpu'
print(device)
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name).to(device)

from difflib import SequenceMatcher

class MathsQuestions:
    @staticmethod
    def __filter_sentences(sentences, original_sentence):
        best_score = float("-inf")
        filtered_sentence = []
        for sentence in sentences:
            score = SequenceMatcher(None, original_sentence, sentence).ratio()
            if score > best_score:
                best_score = score
                filtered_sentence.append(sentence)
        
        return filtered_sentence
    
    @staticmethod
    def __paraphrase_sentence(text, max_length=128, num_return_sequences=5, num_beams=25, temperature=0.7, repetition_penalty=1.5, no_repeat_ngram_size=5):
        input_ids = tokenizer(
            f'paraphrase: {text}',
            return_tensors="pt", 
            padding="longest",
            max_length=max_length,
            truncation=True,
        ).input_ids.to(device)
        
        model_output = model.generate(
            input_ids, 
            temperature=temperature, 
            repetition_penalty=repetition_penalty,
            num_return_sequences=num_return_sequences,
            no_repeat_ngram_size=no_repeat_ngram_size, 
            num_beams=num_beams, 
            max_length=max_length
        )

        return tokenizer.batch_decode(model_output, skip_special_tokens=True)

    @staticmethod
    def parse_template(template: str) -> dict:
        names = KeywordExtraction.get_keywords(template, pos={'PROPN'})
        nouns = KeywordExtraction.get_keywords(template, pos={'NOUN'})
        
        return { "names" : names, "nouns": nouns }

    @staticmethod
    def generate_questions(template: str) -> List[str]:
        template_info = MathsQuestions.parse_template(template)

        question = template

        # Replace Names
        for name in template_info["names"]:
            question = re.sub(name, names.get_first_name(), question, flags=re.IGNORECASE)

        for noun in template_info["nouns"][:1]:
            a = MCQEngine("S", noun).generate_distractors_transformer()
            question = re.sub(noun, random.choice(a).lower(), question, flags=re.IGNORECASE)

        sentences = question.split(".")

        sentence_list = []

        for sentence in sentences:
            new_sentences = MathsQuestions.__paraphrase_sentence(sentence)
            filtered_sentence = MathsQuestions.__filter_sentences(new_sentences, sentence)
            sentence_list.append(filtered_sentence)

        res = set()
        for i in range(len(sentence_list)):
            s = [item[min(i, len(item) - 1)] for item in sentence_list]
            res.add(" ".join(s))

        return list(res)

if __name__ == "__main__":
    sentence = "John, Joe, Sarah are in the park playing football and enjoying the sunny weather. They stop to have some lunch. John currently has 3 apples in his lunchbox and Joe has 2 apples in his lunchbox. Joe is feeling generous and gives 2 apples to John. Sarah also has 9 apples in her lunchbox. John is full and gives 4 apples to Sarah. How many apples does John now have?"
    sentences = MathsQuestions.generate_questions(sentence)
    for s in sentences:
        print(s)
        print()