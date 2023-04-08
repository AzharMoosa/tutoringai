from typing import Tuple, List
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch
from engines.keyword_extraction_engine import KeywordExtraction
from engines.summarization_engine import TextSummarization
from transformers import T5ForConditionalGeneration, T5Tokenizer
from sense2vec import Sense2Vec
import random
from rapidfuzz.distance import Levenshtein
from engines.mcq_engine import MCQEngine
import nltk
import os
nltk.download('omw-1.4')

model = T5ForConditionalGeneration.from_pretrained('ramsrigouthamg/t5_squad_v1')
tokenizer = T5Tokenizer.from_pretrained('ramsrigouthamg/t5_squad_v1')
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Device {device}")
model = model.to(device)

__location__ = os.path.realpath(os.path.join(
    os.getcwd(), os.path.dirname(__file__)))

s2v = Sense2Vec().from_disk(f"{__location__}/s2v")

class TextToQuestion:
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
        max_length = 384
        encoder = tokenizer.encode_plus(text,
                                        max_length=max_length,
                                        pad_to_max_length=False,
                                        truncation=True,
                                        return_tensors="pt").to(device)

        return encoder["input_ids"], encoder["attention_mask"]

    @staticmethod
    def __filter_same_sense(sense: str, words: List[str]) -> List[str]:
        """
        Filters a list of words using a base sense.

        Arguments:
            sense {str} The base sense to use
            words {List[str]} The list of words to filter

        Returns:
            {List[str]} The input ids and the attention mask
        """
        def process_word(word: str) -> str:
            return word[0].split("|")[0].replace("_", " ").title().strip()

        sense = sense.split("|")[1]
        
        return [process_word(word) for word in words if word[0].split("|")[1] == sense]

    @staticmethod
    def __maximum_similarity_score(word: str, words: List[str]):
        """
        Retrieves the maximum similarity score using a word and
        a list of words.

        Arguments:
            word {str} The base word to compare to
            words {List[str]} The list of words to compare to

        Returns:
            {List[str]} The input ids and the attention mask
        """
        return max([Levenshtein.normalized_distance(w.lower(), word.lower()) for w in words])

    @staticmethod
    def __generate_distractors_sense2vec(word: str, question: str, n=40):
        best_sense = s2v.get_best_sense(word, senses=["NOUN", "PERSON", "PRODUCT", "LOC", "ORG", "EVENT", "NORP", "WORK OF ART", "FAC", "GPE", "NUM", "FACILITY"])
        most_similar = TextToQuestion.__filter_same_sense(best_sense, s2v.most_similar(best_sense, n=n))

        threshold = 0.6
        distractors = [word]
        question_token = question.split()

        for word in most_similar:
            if TextToQuestion.__maximum_similarity_score(word, distractors) < threshold and word not in distractors and distractors not in question_token:
                distractors.append(word)
            
        return distractors[1:]
    
    @staticmethod
    def get_mcq_question(text: str, options: int = 4, type: str="transformer") -> dict:
        """
        Generates MCQ questions for a text input.

        Arguments:
            text {str} The base word to compare to
            options {int} The number of options to use in the MCQ
            type {str} The type of method used to generate distractors

        Returns:
            {dict} The mapping of a question to the distractors and the answer
                   to the MCQ question.
        """
        question_list = TextToQuestion.get_question(text)
        mcq_mapping = {}
        for question, answer in question_list:
            if type == "wordnet":
                distractors = MCQEngine(question, answer).generate_distractors_wordnet()
            elif type == "sense2vec":
                distractors = MCQEngine(question, answer).generate_distractors_sense2vec()
            elif type == "transformer":
                distractors = MCQEngine(question, answer).generate_distractors_transformer()
            else:
                distractors = []

            distractors = [answer.capitalize()] + distractors[:options-1]
            random.shuffle(distractors)
            mcq_mapping[question] = (distractors, answer.capitalize())

        return mcq_mapping

    @staticmethod
    def get_question(context: str) -> List[Tuple[str, str]]:
        """
        Generates questions using a given text input

        Arguments:
            context {str} The input text used to generate questions from

        Returns:
            {List[Tuple[str, str]]} A list of questions and answers
        """
        summarized_text = TextSummarization.summarize(context)
        keywords = KeywordExtraction.get_keywords(context)
        question_list = []

        for keyword in keywords:
            text = f"context: {summarized_text} answer: {keyword}"
            input_ids, attention_mask = TextToQuestion.__get_input_ids_attention_mask(text)
            
            model_output = model.generate(input_ids=input_ids,
                                      attention_mask=attention_mask,
                                      early_stopping=True,
                                      num_beams=5,
                                      num_return_sequences=1,
                                      no_repeat_ngram_size=2,
                                      max_length=72)
        
            decoded_output = [tokenizer.decode(id, skip_special_tokens=True) for id in model_output]
            question = decoded_output[0].replace("question:", "").strip()
            question_list.append((question, keyword))

        return question_list
    

if __name__ == "__main__":
    # a = TextToQuestion.get_question("A Lion lay asleep in the forest, his great head resting on his paws. A timid little Mouse came upon him unexpectedly, and in her fright and haste to get away, ran across the Lion's nose. Roused from his nap, the Lion laid his huge paw angrily on the tiny creature to kill her.  \"Spare me!\" begged the poor Mouse. \"Please let me go and some day I will surely repay you.\"  The Lion was much amused to think that a Mouse could ever help him. But he was generous and finally let the Mouse go.  Some days later, while stalking his prey in the forest, the Lion was caught in the toils of a hunter's net. Unable to free himself, he filled the forest with his angry roaring. The Mouse knew the voice and quickly found the Lion struggling in the net. Running to one of the great ropes that bound him, she gnawed it until it parted, and soon the Lion was free. \"You laughed when I said I would repay you,\" said the Mouse. \"Now you see that even a Mouse can help a Lion.")
    # b = TextToQuestion.get_mcq_question("A Lion lay asleep in the forest, his great head resting on his paws. A timid little Mouse came upon him unexpectedly, and in her fright and haste to get away, ran across the Lion's nose. Roused from his nap, the Lion laid his huge paw angrily on the tiny creature to kill her.  \"Spare me!\" begged the poor Mouse. \"Please let me go and some day I will surely repay you.\"  The Lion was much amused to think that a Mouse could ever help him. But he was generous and finally let the Mouse go.  Some days later, while stalking his prey in the forest, the Lion was caught in the toils of a hunter's net. Unable to free himself, he filled the forest with his angry roaring. The Mouse knew the voice and quickly found the Lion struggling in the net. Running to one of the great ropes that bound him, she gnawed it until it parted, and soon the Lion was free. \"You laughed when I said I would repay you,\" said the Mouse. \"Now you see that even a Mouse can help a Lion.")
    # print(b)
    c = TextToQuestion.get_mcq_question("John, Joe, Sarah are playing football. John has 5 apples and Joe has 2 apples. Joe gives 2 apples to John. Sarah has 9 apples. John gives 4 apples to Sarah. How many apples does John have?")
    print(c)