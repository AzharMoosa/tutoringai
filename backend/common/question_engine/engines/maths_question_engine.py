import names
import re
import random
from keyword_extraction_engine import KeywordExtraction
from mcq_engine import MCQEngine
import torch
from transformers import PegasusForConditionalGeneration, PegasusTokenizer
model_name = 'tuner007/pegasus_paraphrase'
device = 'cuda' if torch.cuda.is_available() else 'cpu'
print(device)
tokenizer = PegasusTokenizer.from_pretrained(model_name)
model = PegasusForConditionalGeneration.from_pretrained(model_name).to(device)
from difflib import SequenceMatcher

class MathsQuestions:
    @staticmethod
    def parse_template(template: str):
        names = KeywordExtraction.get_keywords(template, pos={'PROPN'})
        nouns = KeywordExtraction.get_keywords(template, pos={'NOUN'})
        
        return { "names" : names, "nouns": nouns }

    @staticmethod
    def generate_question(template: str):
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
            new_sentences = get_response(sentence, 10, 10)
            filtered_sentence = filter_sentences(new_sentences, sentence)
            sentence_list.append(filtered_sentence)

        res = []
        for i in range(len(sentence_list)):
            s = [item[min(i, len(item) - 1)] for item in sentence_list]
            res.append(" ".join(s))

        return res

def filter_sentences(sentences, original_sentence):
    best_score = float("-inf")
    filtered_sentence = [original_sentence]
    for sentence in sentences:
        score = SequenceMatcher(None, original_sentence, sentence).ratio()
        if score > best_score:
            best_score = score
            filtered_sentence.append(sentence)
    
    return filtered_sentence

def get_response(input_text,num_return_sequences,num_beams):
  batch = tokenizer([input_text],truncation=True,padding='longest',max_length=60, return_tensors="pt").to(device)
  translated = model.generate(**batch,max_length=60,num_beams=num_beams, num_return_sequences=num_return_sequences, temperature=1.5)
  tgt_text = tokenizer.batch_decode(translated, skip_special_tokens=True)
  return tgt_text

if __name__ == "__main__":
    sentence = "John, Joe, Sarah are in the park playing football and enjoying the sunny weather. They stop to have some lunch. John currently has 3 apples in his lunchbox and Joe has 2 apples in his lunchbox. Joe is feeling generous and gives 2 apples to John. Sarah also has 9 apples in her lunchbox. John is full and gives 4 apples to Sarah. How many apples does John now have?"
    a = MathsQuestions.generate_question(sentence)
    # for s in a:
    #     print(s)
    #     print()
    # print(sentence)