from typing import List
import json
import string
import re
import nltk
import pke
from nltk.tokenize import sent_tokenize
from flashtext import KeywordProcessor
nltk.download("punkt")

pos = {'VERB', 'ADJ', 'NOUN'}


class FillInBlankEngine:
    def __init__(self, text: str) -> None:
        self.text = text

    def __tokenize_sentence(self) -> List[str]:
        """
        Tokenizes sentences into sentence tokens.

        Returns:
            {List[str]} The sequence of sentences tokenized into a list
        """
        sentence_tokens = sent_tokenize(self.text)
        sentence_tokens = [sentence.strip()
                           for sentence in sentence_tokens if len(sentence) > 20]
        return sentence_tokens

    def __create_extractor(self, alpha: float = 1.1, threshold: float = 0.75, method: str = "average"):
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
        extractor.load_document(input=self.text, language="en")
        extractor.candidate_selection(pos=pos)
        extractor.candidate_weighting(
            alpha=alpha, threshold=threshold, method=method)
        return extractor

    def __extract_keyphrases(self, n_best: int = 30) -> List[str]:
        """
        Decodes the sentence into a string.

        Arguments:
            n_best {int} The number of best keyphrases the extractor should retrieve

        Returns:
            {List[str]} The keyphrases that are extracted
        """
        try:
            extractor = self.__create_extractor()
            best_keyphrases = extractor.get_n_best(n=n_best)
            return [phrase[0] for phrase in best_keyphrases]
        except:
            raise Exception("ERROR! Unable to extract keyphrases")

    def __get_sentence_mapping(self) -> dict:
        """
        Processes the text into a dictionary mapping of keywords and its
        sentence.

        Returns:
            {dict} The mappings between keywords and its associated sentence.
        """
        processor = KeywordProcessor()
        sentence_mapping = {}

        keywords = self.__extract_keyphrases()
        sentences = self.__tokenize_sentence()

        for keyword in keywords:
            sentence_mapping[keyword] = []
            processor.add_keyword(keyword)

        for sentence in sentences:
            words = processor.extract_keywords(sentence)
            for keyword in words:
                sentence_mapping[keyword].append(sentence)

        for keyword, sentences in sentence_mapping.items():
            sentence_mapping[keyword] = sorted(
                sentences, key=len, reverse=True)

        return sentence_mapping

    def generate_fill_in_the_blank(self, n: int = 10) -> dict:
        """
        Retrieves the keyword and sentence mapping. Removes keywords
        from the sentence to generate a text with blank statements.

        Arguments:
            n {int} The number of sentences with blank statements
        Returns:
            {dict} The dictionary containing the sentence mapping and the 
                   text with blank statements.
        """
        sentence_mapping = self.__get_sentence_mapping()
        result = {}
        masked_sentences = []
        seen = set()
        keywords = []

        for keyword, sentences in sentence_mapping.items():
            if len(sentences) > 0:
                sentence = sentences[0]
                insensitive_sentence = re.compile(
                    re.escape(keyword), re.IGNORECASE)
                replacements = len(re.findall(
                    re.escape(keyword), sentence, re.IGNORECASE))
                mask = insensitive_sentence.sub(" ______ ", sentence)

                if sentence not in seen and replacements < 2:
                    masked_sentences.append(mask)
                    seen.add(sentence)
                    keywords.append(keyword)

        result["sentence_mapping"] = list(
            zip(masked_sentences[:n], keywords[:n]))
        result["text"] = " ".join(masked_sentences[:n])

        return result


if __name__ == "__main__":
    f = FillInBlankEngine("There is a lot of volcanic activity at divergent plate boundaries in the oceans. For example, many undersea volcanoes are found along the Mid-Atlantic Ridge. This is a divergent plate boundary that runs north-south through the middle of the Atlantic Ocean. As tectonic plates pull away from each other at a divergent plate boundary, they create deep fissures, or cracks, in the crust. Molten rock, called magma, erupts through these cracks onto Earth’s surface. At the surface, the molten rock is called lava. It cools and hardens, forming rock. Divergent plate boundaries also occur in the continental crust. Volcanoes form at these boundaries, but less often than in ocean crust. That’s because continental crust is thicker than oceanic crust. This makes it more difficult for molten rock to push up through the crust. Many volcanoes form along convergent plate boundaries where one tectonic plate is pulled down beneath another at a subduction zone. The leading edge of the plate melts as it is pulled into the mantle, forming magma that erupts as volcanoes. When a line of volcanoes forms along a subduction zone, they make up a volcanic arc. The edges of the Pacific plate are long subduction zones lined with volcanoes. This is why the Pacific rim is called the “Pacific Ring of Fire.")
    print(f.generate_fill_in_the_blank()["sentence_mapping"])
