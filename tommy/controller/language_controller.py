from tommy.model.language_model import LanguageModel
from tommy.support.supported_languages import SupportedLanguage


class LanguageController:
    """
    Controls the access to and changes to the selected language for topic
    modelling, and loading the settings from the associated file.
    """
    _language_model: LanguageModel = None

    def set_language_refs(self, language_model: LanguageModel) -> None:
        """Set the reference to the language-model"""
        self._language_model = language_model

    def set_language(self, language: SupportedLanguage) -> None:
        """Set the language for the topic modelling"""
        self._language_model.selectedLanguage = language

    def get_language(self) -> SupportedLanguage:
        """Return the language for the topic modelling"""
        return self._language_model.selectedLanguage

    def get_stopwords_path(self) -> str:
        """Return the path to the stopwords file for the selected language"""
        return f"tommy/data/stopwords/{self.get_language().name}.txt"

    def get_preprocessing_model_name(self) -> str:
        """Return the name of the preprocessing model for the selected language"""
        match self.get_language():
            case SupportedLanguage.Dutch:
                return "nl_core_news_sm-3.7.0"
            case SupportedLanguage.English:
                return "en_core_web_sm-3.7.1"
            case _:
                raise ValueError("Unsupported language")


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University 
(Department of Information and Computing Sciences)
"""
