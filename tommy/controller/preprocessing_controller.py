import os

import spacy
from spacy.tokens import Doc

from tommy.model.stopwords_model import StopwordsModel
from tommy.support.application_settings import application_settings
from tommy.support.supported_languages import SupportedLanguage
from tommy.controller.language_controller import LanguageController


class PreprocessingController:
    """A class that can preprocess text using the Dutch SpaCy pipeline."""
    _stopwords_model: StopwordsModel = None
    _enable_pos: bool

    def __init__(self, language_controller: LanguageController) -> None:
        self._nlp = None
        self._enable_pos: bool
        self.language_controller = language_controller
        self.language_controller.change_language_event.subscribe(
            self.load_pipeline)

    def load_pipeline(self, language: SupportedLanguage) -> None:
        nlp: spacy.Language
        match language:
            case SupportedLanguage.Dutch:
                self._enable_pos = True
                pipeline_path = os.path.join(
                    application_settings.preprocessing_data_folder
                    , "pipeline_download", "nl_core_news_sm-3.7.0")
                nlp = spacy.load(pipeline_path,
                                 exclude=["tagger", "attribute_ruler", "parser",
                                          "senter"])
            case SupportedLanguage.English:
                self._enable_pos = False
                pipeline_path = os.path.join(
                    application_settings.preprocessing_data_folder,
                    "pipeline_download", "en_core_web_sm-3.7.1")
                # tagger is taking over the role of the morphologizer (
                # supposedly)
                nlp = spacy.load(pipeline_path, exclude=["parser", "senter"])
            case _:
                raise ValueError("Unsupported preprocessing language")
        self._nlp = nlp

        # TODO: refine the entity set (i.e. "proper-noun filtering")
        self._entity_categories = {"PERSON", "FAC", "LAW", "TIME", "PERCENT",
                                   "MONEY", "QUANTITY", "ORDINAL", "CARDINAL"}
        self._pos_categories = {"NOUN", "PROPN", "ADJ", "ADV", "VERB"}

    def set_model_refs(self, stopwords_model: StopwordsModel):
        self._stopwords_model = stopwords_model

    def process_text(self, text: str) -> list[str]:
        """Preprocesses the given text to a list of tokens."""
        tokens = self._nlp(text)
        tokens = self.process_tokens(tokens)
        return tokens

    def process_tokens(self, doc: Doc) -> list[str]:
        """
        Processes the tokens given by the SpaCy pipeline.

        :param doc: The tokens given by processing of the Dutch SpaCy pipeline
        :return list[str]: The processed tokens
        """
        # 2, 3, 4 - all steps that require token-level information
        lemmas = [token.lemma_ for token in doc if
                  token.ent_type_ not in self._entity_categories and (
                          not self._enable_pos or
                          token.pos_ in self._pos_categories)]

        # 5 - transforming the tokens (lemmas) themselves
        lemmas = [lemma.lower() for lemma in lemmas if len(lemma) > 3]
        # TODO: fine-grain abbreviation filtering (i.e. don't exclude
        #  every token under 4 characters)

        # TODO: fix "-"words and remove diacritical marks
        #  (i.e. character 'normalization')

        # 8 - stopword removal
        lemmas = self.filter_stopwords(lemmas)

        return lemmas

    def filter_stopwords(self, tokens: list[str]) -> list[str]:
        """
        Removes all stopwords from the given list of tokens.

        :param tokens: The list of tokens
        :return: The list of tokens without stopwords
        """
        return [token for token in tokens if
                token not in self._stopwords_model]


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University
(Department of Information and Computing Sciences)
"""
