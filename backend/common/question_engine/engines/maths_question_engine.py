import names
import re
from typing import List
import random
from engines.keyword_extraction_engine import KeywordExtraction
from engines.mcq_engine import MCQEngine
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from engines.solving_engine import SolvingEngine
model_name = "humarin/chatgpt_paraphraser_on_T5_base"
device = 'cuda' if torch.cuda.is_available() else 'cpu'
print(device)
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name).to(device)
import inflect
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
    def paraphrase_sentence(text, max_length=128, num_return_sequences=5, num_beams=25, temperature=0.7, repetition_penalty=1.5, no_repeat_ngram_size=5):
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
    def normalise_numbers(text: str) -> str:
        p = inflect.engine()
        numbers = re.findall(r'\d+', text)
        for num in set(numbers):
            word = p.number_to_words(num)
            text = text.replace(num, word)

        return text
    
    @staticmethod
    def __randomize_numbers(text: str):
        numbers = re.findall(r'\d+', text)

        for number in numbers:
            new_number = str(random.randint(1, 10))
            text = text.replace(number, new_number)
        
        return text

    @staticmethod
    def generate_questions(template: dict, variants: int = 10) -> List[tuple]:
        text = template["text"]
        template_info = MathsQuestions.parse_template(text)
        questions = []

        for _ in range(variants):
            question = MathsQuestions.normalise_numbers(text)
            answer = SolvingEngine.solve(text, template["type"])
            # Replace Names
            for name in template_info["names"]:
                question = re.sub(name, names.get_first_name(), question, flags=re.IGNORECASE)

            for noun in template_info["nouns"][:1]:
                a = MCQEngine("S", noun).generate_distractors_transformer()
                question = re.sub(noun, random.choice(a).lower(), question, flags=re.IGNORECASE)

            sentences = question.split(".")

            sentence_list = []

            for sentence in sentences:
                new_sentences = MathsQuestions.paraphrase_sentence(sentence)
                filtered_sentence = MathsQuestions.__filter_sentences(new_sentences, sentence)
                sentence_list.append(filtered_sentence)

            res = set()
            for i in range(len(sentence_list)):
                s = [item[min(i, len(item) - 1)] for item in sentence_list]
                res.add(" ".join(s))

            questions.extend([(question, answer) for question in res])

            text = MathsQuestions.__randomize_numbers(text)

        return questions

if __name__ == "__main__":
    template = { "type": "additive", "text" : "John, Joe, Sarah are in the park playing football and enjoying the sunny weather. They stop to have some lunch. John has 3 apples in his lunchbox. Joe has 2 apples in his lunchbox. Joe is feeling generous and gives 2 apples to John. Sarah also has 9 apples in her lunchbox. John is full and gives 4 apples to Sarah. How many apples does John now have?"
 }
    questions = MathsQuestions.generate_questions(template)
    for question, answer in questions:
        print(question)
        print(answer)
        print()
    