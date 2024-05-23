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
    _change_language_event: EventHandler[SupportedLanguage] = None
    _language_model_changed_event: EventHandler[None] = EventHandler()

    @property
    def language_model_changed_event(self) -> EventHandler[None]:
        """
        The event that is triggered when the language model is changed
        for example due to changing configs
        :return: The event
        """
        return self._language_model_changed_event

    @property
    def change_language_event(self) -> EventHandler[SupportedLanguage]:
        return self._change_language_event

    def __init__(self) -> None:
        self._change_language_event = EventHandler[SupportedLanguage]()

    def set_model_refs(self, language_model: LanguageModel) -> None:
        """Set the reference to the language-model"""
        self._language_model = language_model
        self._change_language_event.publish(language_model.selected_language)

    def change_config_model_refs(self, language_model: LanguageModel) -> None:
        """
        Set the reference to the language-model and update the frontend
        """
        self._language_model = language_model
        self._language_model_changed_event.publish(None)

    def set_language(self, language: SupportedLanguage) -> None:
        """Set the language for the topic modelling"""
        self._language_model.selected_language = language
        self._change_language_event.publish(language)

    def get_language(self) -> SupportedLanguage:
        """Return the language for the topic modelling"""
        return self._language_model.selected_language


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University 
(Department of Information and Computing Sciences)
"""
