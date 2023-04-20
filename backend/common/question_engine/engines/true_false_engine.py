from typing import Tuple, List
import re
import spacy
from allennlp.predictors.predictor import Predictor
import allennlp_models.tagging
import nltk
from nltk import tokenize
from nltk.tree import Tree
import tensorflow as tf
from transformers import TFGPT2LMHeadModel, GPT2Tokenizer
from backend.common.question_engine.engines.maths_question_engine import MathsQuestions

NOUN_PHRASE = "NP"
VERB_PHRASE = "VP"
PREDICTOR_PATH = "https://storage.googleapis.com/allennlp-public-models/elmo-constituency-parser-2020.02.10.tar.gz"

# Download NLTK
nltk.download("punkt")

# Load Predictor
predictor = Predictor.from_path(PREDICTOR_PATH)
nlp = spacy.load("en_core_web_sm")

# Load GPT2 Model
GPT2_TOKENIZER = GPT2Tokenizer.from_pretrained("gpt2")
GPT2_MODEL = TFGPT2LMHeadModel.from_pretrained(
    "gpt2", pad_token_id=GPT2_TOKENIZER.eos_token_id)


class TrueOrFalseEngine:
    @staticmethod
    def __flatten_tree(tree: Tree) -> str:
        """
        Flattens the incoming tree into a string.

        Arguments:
            tree {Tree} The input tree to be parsed.

        Returns:
            {str} The resulting string formed from the tree.
        """
        if not tree:
            return ""

        statements = [" ".join(t.leaves()) for t in list(tree)]

        return " ".join(statements)


    @staticmethod
    def __get_verb_noun_phrase(tree: Tree, verb_phrase: str = None, noun_phrase: str = None) -> Tuple[str, str]:
        """
        Gets the rightmost verb and noun phrase from a sentence.
        The function traverses the tree using the right most
        subtree and returns the verb and noun phrase at the
        leaf node.

        Arguments:
            tree {Tree} The input tree to be parsed.
            verb_phrase {str} The most recent verb phrase.
            noun_phrase {str} The most recent noun phrase.

        Returns:
            {Tuple[str, str]} The rightmost verb and noun phrase.
        """
        if len(tree.leaves()) == 1:
            return verb_phrase, noun_phrase

        right_tree = tree[-1]

        if right_tree.label() == VERB_PHRASE:
            verb_phrase = right_tree
        elif right_tree.label() == NOUN_PHRASE:
            noun_phrase = right_tree

        return TrueOrFalseEngine.__get_verb_noun_phrase(right_tree, verb_phrase, noun_phrase)

    @staticmethod
    def __remove_phrase(sentence: str, phrase: str) -> str:
        """
        Locates the phrase in a sentence and removes it to
        return a partial sentence with the phrase removed.

        Arguments:
            sentence {str} The full sentence that is being processed
            phrase {str} The phrase to be removed from the sentence

        Returns:
            {str} The partial sentence with the phrase removed from 
                  the original string.
        """
        phrase = phrase.replace(" ", "")
        sentence_tokens = sentence.split()

        # Locate Phrase
        for i in range(len(sentence_tokens)):
            last_phrase = "".join(sentence_tokens[i:]).replace(" ", "")
            if last_phrase == phrase:
                # Remove Phrase From Sentence
                return " ".join(sentence_tokens[:i])

        return ""

    @staticmethod
    def __process_phrase(phrase: str) -> str:
        """
        Replaces any left or right brackets from the string.

        Arguments:
            phrase {str} The phrase to be processed

        Returns:
            {str} The phrase after is has been processed.
        """
        phrase = re.sub(r"-LRB- ", "(", phrase)
        phrase = re.sub(r" -RRB-", ")", phrase)
        return phrase

    @staticmethod
    def __get_partial_sentence(statement: str) -> str:
        """
        The algorithm first starts by find the rightmost verb
        and noun phrase. Then the tree is flattened into a
        string. The phrase with the longest length is selected
        and removed from the original sentence.

        Returns:
            {str} The partial sentence with either the verb or
                  noun phrase removed.
        """
        cleaned_statement = statement.rstrip("?:!.,;")
        parsed_statement = predictor.predict(sentence=cleaned_statement)
        tree = Tree.fromstring(parsed_statement["trees"])
        verb_phrase, noun_phrase = TrueOrFalseEngine.__get_verb_noun_phrase(tree)
        verb_phrase, noun_phrase = TrueOrFalseEngine.__flatten_tree(
            verb_phrase), TrueOrFalseEngine.__flatten_tree(noun_phrase)
        phrase = max(verb_phrase, noun_phrase, key=len)
        phrase = TrueOrFalseEngine.__process_phrase(phrase)
        partial_sentence = TrueOrFalseEngine.__remove_phrase(cleaned_statement, phrase)

        return partial_sentence

    @staticmethod
    def __generate_sentences(partial_sentence: str,
                             additional_characters: int = 40,
                             do_sample: bool = True,
                             top_p: float = 0.8,
                             top_k: int = 30,
                             repetition_penalty: float = 10.0,
                             num_return_sequences: int = 3) -> tf.float32:
        """
        Generates sentences using GPT2 based on the incoming partial
        sentence.

        Arguments:
            partial_sentence {str} The partial sentence to be completed
            additional_characters {int} The number of additional characters
                                        that can be added
            do_sample {bool} Whether or not to use sampling
            top_p {float} If set to float < 1, only the smallest set
                          of most probable tokens with probabilities 
                          that add up to top_p or higher are kept 
                          for generation
            top_k {int} The number of highest probability vocabulary tokens to keep for top-k-filtering
            repetition_penalty {float} The parameter for repetition penalty 
            num_return_sequences {int} The number of independently computed returned sequences for each element in the batch

        Returns:
            {tf.float32} The tensor containing the generated sentences.
        """
        ids = GPT2_TOKENIZER.encode(partial_sentence, return_tensors="tf")
        sentence_length = len(partial_sentence.split()) + additional_characters
        return GPT2_MODEL.generate(
            ids,
            do_sample=do_sample,
            max_length=sentence_length,
            top_p=top_p,
            top_k=top_k,
            repetition_penalty=repetition_penalty,
            num_return_sequences=num_return_sequences
        )

    @staticmethod
    def __decode_sentence(sentence: tf.float32) -> str:
        """
        Decodes the sentence into a string.

        Arguments:
            sentence {tf.float32} The decoded tensor

        Returns:
            {str} The decoded sentence as a string.
        """
        decoded_sentence = GPT2_TOKENIZER.decode(
            sentence, skip_special_tokens=True)
        return tokenize.sent_tokenize(decoded_sentence)[0]


    @staticmethod
    def generate_false_options(statement: str) -> List[Tuple[str, str]]:
        """
        Generates false statements using the original true
        statement. First the sentence is split into a partial
        sentence. Then GPT2 model is used to generate false
        statements using the partial statement.

        Returns:
            {List[str]} The list of false statements.
        """
        true_statement = MathsQuestions.paraphrase_sentence(statement)

        # Get Partial Sentence With Verb or Noun Phrase Removed
        partial_sentence = TrueOrFalseEngine.__get_partial_sentence(statement)

        # Generate Sentences Using GPT-2
        generated_sentences = TrueOrFalseEngine.__generate_sentences(partial_sentence)

        false_options = [(true_statement, TrueOrFalseEngine.__decode_sentence(
            sentence)) for sentence in generated_sentences]

        return false_options


if __name__ == "__main__":
    TrueOrFalseEngine.generate_false_options("John, Joe, Sarah are in the park playing football and enjoying the sunny weather.")
