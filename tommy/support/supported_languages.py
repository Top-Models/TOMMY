from __future__ import annotations

from enum import Enum


class SupportedLanguage(Enum):
    """An enumeration of the supported languages."""
    Dutch = 1
    English = 2

    @staticmethod
    def from_string(language: str) -> SupportedLanguage:
        """
        Convert a string to a SupportedLanguage.
        :param language: The string to convert
        :return: The SupportedLanguage
        """
        match language:
            case "Nederlands":
                return SupportedLanguage.Dutch
            case "Engels":
                return SupportedLanguage.English
            case _:
                raise ValueError(f"Language {language} not recognized")

    @staticmethod
    def to_string(language: SupportedLanguage) -> str:
        """
        Convert a SupportedLanguage to a string.
        :param language: The SupportedLanguage to convert
        :return: The string
        """
        match language:
            case SupportedLanguage.Dutch:
                return "Nederlands"
            case SupportedLanguage.English:
                return "Engels"
            case _:
                raise ValueError(f"Language {language} not recognized")

"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University
(Department of Information and Computing Sciences)
"""
