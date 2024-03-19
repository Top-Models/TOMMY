import os
import spacy
from collections.abc import Iterable
from spacy.tokens import Doc

from interactive_topic_modeling.backend.preprocessing.stopwords import (
    StopWords)
from interactive_topic_modeling.support.project_settings import (
    current_project_settings)


#    Entire pipeline:
#    ----------------
# 1. Build-in tokenization (generates metadata)
# 2. Remove certain entity types
# 3. Remove certain POS categories
# 4. Take the lemmas of the tokens
# 5. Convert to lowercase, remove 1-letter words, remove diacritical marks
#    (i.e. additional tokenization)
# 6. TODO: Implement n-grams (up to some n)                        (Gensim)
# 7. TODO: Implement word-frequency filtering (w/ some threshold)  (Gensim)
# 8. Remove lemmatized stopwords

class Pipeline:
    """Text preprocessing pipeline."""

    def __init__(self) -> None:
        """
        Initialize the pipeline.
        Used components: tok2vec, lemmatizer, tagger, attribute-ruler, ner
        """
        # Load pre-trained natural language pipeline (python3 -m spacy
        # download nl_core_news_sm)
        # TODO: optimize by downloading the model at another place
        #  (maybe use spacy_download)
        pipeline_path = os.path.join(
            current_project_settings.preprocessing_data_folder,
            "pipeline_download", "nl_core_news_sm-3.7.0")
        nlp = spacy.load(pipeline_path, exclude=["tagger",
                                                 "attribute_ruler",
                                                 "parser",
                                                 "senter"])
        self._nlp = nlp

        self._entity_categories = {"PERSON", "FAC", "LAW", "TIME", "PERCENT",
                                   "MONEY", "QUANTITY", "ORDINAL", "CARDINAL"}
        # TODO: refine the entity set (i.e. "proper-noun filtering")
        self._pos_categories = {"NOUN", "PROPN", "ADJ", "ADV", "VERB"}

        # Load stopwords
        with open(os.path.join(
                current_project_settings.preprocessing_data_folder,
                "stopwords.txt"), 'r') as file:
            file_content = file.read()

        stopword_list = file_content.split()
        self._stopwords = StopWords(stopword_list)
        # TODO: keep track of added stopwords

    # def __call__(self, text: str) -> list[str]:
    """Process the text to tokens"""

    #    tokens = self._nlp(text)
    #    tokens = self.process_tokens(tokens)
    #    return tokens

    # Function for quick preprocessing (used when debugging plots for example)
    def __call__(self, text: str) -> list[str]:
        """
        Process the text to tokens.

        :param text: The text to process.
        :return:
        """
        tokens = set(text.lower().split())
        remove_these = ["hebben", "heeft", "volgens", "wordt", "kunnen", "bekijk", "moeten", "worden", "omdat", "tegen",
                        "onder", "zouden", "waarin", "andere", "waren", "komen", "alleen", "steeds", "tijdens",
                        "pagina:", "oorspronkelijke", "zijn.", "bodegraven.", "werken", "maakt", "waarvan"]
        for token in tokens.copy():
            if len(token) <= 4 or token in remove_these or token in self._stopwords:
                tokens.remove(token)
        return list(tokens)

    def process_tokens(self, doc: Doc) -> list[str]:
        """
        Process the tokens.

        :param doc: The tokens of the doc.
        :return list[str]: The processed tokens.
        """
        # 2, 3, 4 - all steps that require token-level information
        lemmas = [token.lemma_ for token in doc if
                  token.ent_type_ not in self._entity_categories and
                  token.pos_ in self._pos_categories]
        # TODO: look at pos tags (i.e. fine-grained pos i/p coarse-grained pos)

        # 5 - transforming the tokens (lemmas) themselves
        lemmas = [lemma.lower() for lemma in lemmas if len(lemma) > 3]
        # TODO: fine-grain abbreviation filtering (i.e. don't exclude
        #  every token under 4 characters)

        # TODO: fix "-"words and remove diacritical marks
        #  (i.e. character 'normalization')

        # TODO: 6,7

        # 8 - stopword removal, which can should be detached from the
        # rest of the pipeline
        lemmas = [lemma for lemma in lemmas if lemma not in self._stopwords]

        return lemmas

    # TODO: make *args i/o words
    def add_stopwords(self, words: str | Iterable[str]) -> None:
        """Add stopwords to the pipeline."""
        self._stopwords.add(words)

    def remove_stopwords(self, words: str | Iterable[str]) -> None:
        """Remove stopwords from the pipeline."""
        self._stopwords.remove(words)


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University 
(Department of Information and Computing Sciences)
"""
