from typing import List
import nltk
nltk.download("stopwords")
from nltk.corpus import stopwords
from flashtext import KeywordProcessor
import string
import pke
from backend.common.question_engine.engines.summarization_engine import TextSummarization

class KeywordExtraction:
    @staticmethod
    def __create_extractor(text: str, pos: dict, alpha: float = 1.1, threshold: float = 0.75, method: str = "average"):
        """
        Decodes the sentence into a string.

        Arguments:
            alpha {float} The alpha parameter for the extractor
            threshold {float} The threshold parameter for the extractor
            method {str} The method parameter for the extractor

        Returns:
            {extractor} The keyphrase extractor
        """
        extractor = pke.unsupervised.MultipartiteRank()
        extractor.load_document(input=text, language="en")
        extractor.candidate_selection(pos=pos)
        extractor.candidate_weighting(
            alpha=alpha, threshold=threshold, method=method)
        return extractor

    @staticmethod
    def __get_keyphrases(text: str, n_best: int = 15, pos: dict = {'PROPN', 'NOUN'}) -> List[str]:
        """
        Extracts keyphrases from a input text

        Arguments:
            text {str} The input text to get keyphrases from
            n_best {int} The number of keyphrases the extractor should retrieve
            pos {dict} The types of words to look for

        Returns:
            {List[str]} The keyphrases extracted from a text
        """
        try:
            extractor = KeywordExtraction.__create_extractor(text, pos)
            best_keyphrases = extractor.get_n_best(n=n_best)
            return [phrase[0] for phrase in best_keyphrases]
        except:
            raise Exception("ERROR! Unable to extract keyphrases")

    @staticmethod
    def __get_summarized_keywords(keywords: List[str], summarized_text: str) -> List[str]:
        """
        Extracts nouns from a summarized text

        Arguments:
            keywords {List[str]} The keywords from the original text
            summarized_text {str} The summarized input text

        Returns:
            {List[str]} The keyphrases extracted from a summarized text
        """
        processor = KeywordProcessor()
        for keyword in keywords:
            processor.add_keyword(keyword)
        
        return list(set(processor.extract_keywords(summarized_text)))
        
    
    @staticmethod
    def get_keywords(text: str, top: int = 4, pos: dict = {'PROPN', 'NOUN'}):
        """
        Extracts keywords from an input text.

        Arguments:
            text {str} The input text to extract keywords from
            top {int} The maximum number of keywords to retrieve
            pos {dict} The types of words to look for

        Returns:
            {List[str]} The keyphrases extracted from a summarized text
        """
        keyphrases = KeywordExtraction.__get_keyphrases(text, pos=pos)
        summarized_text = TextSummarization.summarize(text)
        summarized_keywords = KeywordExtraction.__get_summarized_keywords(keyphrases, summarized_text)
        keywords = []

        for keyword in keyphrases:
            if keyword in summarized_keywords:
                keywords.append(keyword)
        
        return keywords[:min(top, len(keywords))]


if __name__ == "__main__":
    print(KeywordExtraction.get_keywords("John, Joe, Sarah are playing football. John has 3 apple and Joe has 2 apples. Joe gives 2 apples to John. Sarah has 9 apples. John gives 4 apples to Sarah. How many apples does John have?"))     