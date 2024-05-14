import os

from tommy.controller.language_controller import LanguageController
from tommy.model.stopwords_model import StopwordsModel
from tommy.support.application_settings import application_settings
from tommy.support.supported_languages import SupportedLanguage


class StopwordsController:
    """A class that handles all stopword related functionality."""
    _stopwords_model: StopwordsModel
    _language_controller: LanguageController

    @property
    def stopwords_model(self) -> StopwordsModel:
        return self._stopwords_model

    def __init__(self, language_controller: LanguageController) -> None:
        """Initializes the stopwords controller, and load the stopwords of
        the selected language"""
        self._language_controller = language_controller
        self._language_controller.change_language_event.subscribe(
            self.load_default_stopwords)

    def set_model_refs(self, stopwords_model: StopwordsModel):
        """Sets the reference to the stopwords model."""
        self._stopwords_model = stopwords_model

    def load_default_stopwords(self, language: SupportedLanguage) -> None:
        """Load the default stopwords of the selected language"""
        with open(self.get_stopwords_path(language), 'r') as file:
            file_content = file.read()
        stopword_list = file_content.split()
        self._stopwords_model.default_words = set(stopword_list)

    @staticmethod
    def get_stopwords_path(language: SupportedLanguage) -> str:
        """Return the path to the stopwords file for the selected language"""
        return os.path.join(application_settings.preprocessing_data_folder,
                            "stopwords", f"{language.name}.txt")

    def update_stopwords(self, words: set[str]) -> None:
        """
        Update the stopwords model with a new list of extra stopwords.

        :param words: The new list of stopwords
        :return: None
        """

        self._stopwords_model.replace(words)


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University
(Department of Information and Computing Sciences)
"""
