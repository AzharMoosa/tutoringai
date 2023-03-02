from typing import List
import nltk
nltk.download("stopwords")
from nltk.corpus import stopwords
from flashtext import KeywordProcessor
import string
import pke
from summarization_engine import TextSummarization

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

    def __get_nouns(text: str, n_best: int = 15) -> List[str]:
        """
        Extracts nouns from a input text

        Arguments:
            text {str} The input text to get nouns from
            n_best {int} The number of keyphrases the extractor should retrieve

        Returns:
            {List[str]} The keyphrases extracted from a text
        """
        try:
            extractor = KeywordExtraction.__create_extractor(text, {'PROPN', 'NOUN'})
            best_keyphrases = extractor.get_n_best(n=n_best)
            return [phrase[0] for phrase in best_keyphrases]
        except:
            raise Exception("ERROR! Unable to extract keyphrases")

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
    def get_keywords(text: str, top: int = 4):
        """
        Extracts keywords from an input text.

        Arguments:
            text {str} The input text to extract keywords from
            top {int} The maximum number of keywords to retrieve

        Returns:
            {List[str]} The keyphrases extracted from a summarized text
        """
        nouns = KeywordExtraction.__get_nouns(text)
        summarized_text = TextSummarization.summarize(text)
        summarized_keywords = KeywordExtraction.__get_summarized_keywords(nouns, summarized_text)
        keywords = []

        for keyword in nouns:
            if keyword in summarized_keywords:
                keywords.append(keyword)
        
        return keywords[:min(top, len(keywords))]


if __name__ == "__main__":
    print(KeywordExtraction.get_keywords("A Lion lay asleep in the forest, his great head resting on his paws. A timid little Mouse came upon him unexpectedly, and in her fright and haste to get away, ran across the Lion's nose. Roused from his nap, the Lion laid his huge paw angrily on the tiny creature to kill her.  \"Spare me!\" begged the poor Mouse. \"Please let me go and some day I will surely repay you.\"  The Lion was much amused to think that a Mouse could ever help him. But he was generous and finally let the Mouse go.  Some days later, while stalking his prey in the forest, the Lion was caught in the toils of a hunter's net. Unable to free himself, he filled the forest with his angry roaring. The Mouse knew the voice and quickly found the Lion struggling in the net. Running to one of the great ropes that bound him, she gnawed it until it parted, and soon the Lion was free. \"You laughed when I said I would repay you,\" said the Mouse. \"Now you see that even a Mouse can help a Lion."))     