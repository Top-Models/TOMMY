import os

import spacy
from spacy.tokens import Doc
import nltk
import nltk.data

from tommy.model.stopwords_model import StopwordsModel
from tommy.model.synonyms_model import SynonymsModel
from tommy.support.application_settings import application_settings
from tommy.support.supported_languages import SupportedLanguage
from tommy.controller.language_controller import LanguageController


class PreprocessingController:
    """A class that can preprocess text using the Dutch SpaCy pipeline."""
    _stopwords_model: StopwordsModel = None
    _enable_pos: bool
    _synonyms_model: SynonymsModel = None

    def __init__(self) -> None:
        self._pos_categories = None
        self._entity_categories = None
        self._nlp = None
        self._enable_pos: bool
        self.language_controller = None

        # load punkt tokenizers for splitting sentences
        self._dutch_sent_tokenizer = self._load_nltk_sent_tokenizer(
            "dutch.pickle")
        self._english_sent_tokenizer = self._load_nltk_sent_tokenizer(
            "english.pickle")

    @staticmethod
    def _load_nltk_sent_tokenizer(*path_parts) -> nltk.PunktSentenceTokenizer:
        """
        Load a sentence tokenizer from nltk from the preprocessing data folder
        :param path_parts: Components of the path to the desired tokenizer,
            e.g., "dutch.pickle"
        """
        fpath = f"file:///{os.path.join(
                           application_settings.data_folder,
                           "preprocessing_data", "nltk_downloads", 
                           "tokenizers_punkt", *path_parts)}"
        try:
            tokenizer = nltk.data.load(fpath)
        except LookupError:
            raise LookupError(f"Could not load nltk tokenizer at path {fpath}")
        return tokenizer

    def load_pipeline(self, language: SupportedLanguage) -> None:
        nlp: spacy.Language
        match language:
            case SupportedLanguage.Dutch:
                self._enable_pos = True
                pipeline_path = os.path.join(
                    application_settings.data_folder,
                    "preprocessing_data", "pipeline_download",
                    "nl_core_news_sm-3.7.0")
                nlp = spacy.load(pipeline_path,
                                 exclude=["parser", "tagger",
                                          "attribute_ruler"])
            case SupportedLanguage.English:
                self._enable_pos = False
                pipeline_path = os.path.join(
                    application_settings.data_folder,
                    "preprocessing_data", "pipeline_download",
                    "en_core_web_sm-3.7.1")
                # tagger is taking over the role of the morphologizer (
                # supposedly)
                nlp = spacy.load(pipeline_path, exclude=["parser"])
            case _:
                raise ValueError("Unsupported preprocessing language")
        self._nlp = nlp
        self._nlp.add_pipe("merge_entities")
        self._entity_categories = {"PERSON", "FAC", "LAW", "TIME", "PERCENT",
                                   "MONEY", "QUANTITY", "ORDINAL", "CARDINAL"}
        self._pos_categories = {"NOUN", "PROPN", "ADJ", "ADV", "VERB"}

    def set_model_refs(self, stopwords_model: StopwordsModel,
                       synonyms_model: SynonymsModel) -> None:
        self._stopwords_model = stopwords_model
        self._synonyms_model = synonyms_model

    def set_controller_refs(self, language_controller: LanguageController):
        """Set the reference to the language controller"""
        self.language_controller = language_controller
        self.language_controller.change_language_event.subscribe(
            self.load_pipeline)
        self.load_pipeline(self.language_controller.get_language())

    def process_text(self, text: str) -> list[str]:
        """Preprocesses the given text to a list of tokens."""
        tokens = self._nlp(text)
        tokens = self.process_tokens(tokens)
        return tokens

    def split_into_sentences(self, text: str) -> list[str]:
        """Split the given text to a list of sentences."""
        match self.language_controller.get_language():
            case SupportedLanguage.Dutch:
                tokenizer = self._dutch_sent_tokenizer
            case SupportedLanguage.English:
                tokenizer = self._english_sent_tokenizer
            case _:
                raise ValueError("Current language is not supported by NLTK"
                                 " sentence splitter.")
        return tokenizer.tokenize(text)

    def process_tokens(self, doc: Doc) -> list[str]:
        """
        Processes the tokens given by the SpaCy pipeline.

        :param doc: The tokens given by processing of the Dutch SpaCy pipeline
        :return list[str]: The processed tokens
        """
        # All steps that require token-level information.
        lemmas = [token.lemma_ for token in doc if
                  token.ent_type_ not in self._entity_categories and
                  not str.isspace(token.lemma_) and (
                          not self._enable_pos or
                          token.pos_ in self._pos_categories)]

        # Take the lemmas.
        lemmas = [lemma.lower() for lemma in lemmas if len(lemma) > 2]

        # Apply synonyms and filter stopwords.
        lemmas = self.apply_synonyms(lemmas)
        lemmas = self.filter_stopwords(lemmas)

        return lemmas

    def apply_synonyms(self, tokens: list[str]) -> list[str]:
        """
        Applies synonyms to the given list of tokens.

        :param tokens: The list of tokens
        :return: The list of tokens where tokens are mapped to their synonyms
        """
        return (list(map(
            lambda token: self._synonyms_model.get(token, token), tokens)))

    def filter_stopwords(self, tokens: list[str]) -> list[str]:
        """
        Removes all stopwords from the given list of tokens.

        :param tokens: The list of tokens
        :return: The list of tokens without stopwords
        """
        return [token for token in tokens
                if token not in self._stopwords_model]


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University
(Department of Information and Computing Sciences)
"""
