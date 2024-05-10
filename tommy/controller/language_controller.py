import os.path

from tommy.model.language_model import LanguageModel
from tommy.support.application_settings import application_settings
from tommy.support.supported_languages import SupportedLanguage
from tommy.support.event_handler import EventHandler


class LanguageController:
    """
    Controls the access to and changes to the selected language for topic
    modelling, and loading the settings from the associated file.
    """
    _language_model: LanguageModel = None
    _model_change_language: EventHandler[SupportedLanguage] = None

    @property
    def change_language_event(self) -> EventHandler[SupportedLanguage]:
        return self._model_change_language

    def __init__(self) -> None:
        self._model_change_language = EventHandler[SupportedLanguage]()

    def set_model_refs(self, language_model: LanguageModel) -> None:
        """Set the reference to the language-model"""
        self._language_model = language_model
        self._model_change_language.publish(language_model.selectedLanguage)

    def set_language(self, language: SupportedLanguage) -> None:
        """Set the language for the topic modelling"""
        self._language_model.selectedLanguage = language
        self._model_change_language.publish(language)

    def get_language(self) -> SupportedLanguage:
        """Return the language for the topic modelling"""
        return self._language_model.selectedLanguage


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University 
(Department of Information and Computing Sciences)
"""
