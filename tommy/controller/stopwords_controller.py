import os

from tommy.controller.language_controller import LanguageController
from tommy.model.stopwords_model import StopwordsModel
from tommy.support.event_handler import EventHandler
from tommy.support.application_settings import application_settings
from tommy.support.supported_languages import SupportedLanguage


class StopwordsController:
    """A class that handles all stopword related functionality."""
    _stopwords_model: StopwordsModel
    _language_controller: LanguageController
    _stopwords_model_changed_event: EventHandler[list[str]] = EventHandler()

    @property
    def stopwords_model_changed_event(self) -> EventHandler[list[str]]:
        """This event gets triggered when the stopwords model is changed due
        to the user switching config"""
        return self._stopwords_model_changed_event

    @property
    def stopwords_model(self) -> StopwordsModel:
        return self._stopwords_model

    def __init__(self) -> None:
        """Initializes the stopwords controller, and load the stopwords of
        the selected language"""
        self._language_controller = None

    def set_model_refs(self, stopwords_model: StopwordsModel):
        """Sets the reference to the stopwords model."""
        self._stopwords_model = stopwords_model

    def set_controller_refs(self, language_controller: LanguageController):
        """Sets the reference to the language controller."""
        self._language_controller = language_controller
        language_controller.change_language_event.subscribe(
            self.load_default_stopwords)
        self.load_default_stopwords(language_controller.get_language())

    def on_model_swap(self):
        """
        Notify the frontend that the stopwords model has changed
        :return:
        """
        self._stopwords_model_changed_event.publish(
            self._stopwords_model.extra_words_in_order)

    def load_default_stopwords(self, language: SupportedLanguage) -> None:
        """Load the default stopwords of the selected language"""
        with open(self.get_stopwords_path(language), 'r') as file:
            file_content = file.read()
        stopword_list = file_content.split()
        self._stopwords_model.default_words = set(stopword_list)

    @staticmethod
    def get_stopwords_path(language: SupportedLanguage) -> str:
        """Return the path to the stopwords file for the selected language"""
        return os.path.join(application_settings.data_folder,
                            "preprocessing_data", "stopwords",
                            f"{language.name}.txt")

    def update_stopwords(self, words: list[str]) -> None:
        """
        Update the stopwords model with a new list of extra stopwords.

        :param words: The new list of stopwords
        :return: None
        """
        word_set = set([word.lower() for word in words])
        self._stopwords_model.replace(word_set, words)


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University
(Department of Information and Computing Sciences)
"""
