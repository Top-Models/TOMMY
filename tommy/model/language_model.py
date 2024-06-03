from dataclasses import dataclass
from tommy.support.supported_languages import SupportedLanguage


@dataclass
class LanguageModel:
    """A class representing the supported languages for topic modelling ."""
    selected_language: SupportedLanguage = SupportedLanguage.Dutch


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University 
(Department of Information and Computing Sciences)
"""
