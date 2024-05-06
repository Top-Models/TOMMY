import os
from collections.abc import Iterable

from tommy.support.application_settings import application_settings


class SynonymsModel:
    """
    A class representing the set of synonyms.

    The class acts as a wrapper around a set of synonyms, providing basic
    iterable-like functionality. Initially it represents the set of
    basic/general stopwords imported from a text file, but extra words may
    be added, removed or replaced.
    """

    @property
    def synonyms(self) -> dict[str, list[str]]:
        return self._synonyms_dict

    def __init__(self) -> None:
        """Initializes the SynonymsModel."""
        self._synonyms_dict = {}

    def __len__(self) -> int:
        """Gets the number of main words in the synonyms."""
        return len(self._synonyms_dict)

    def __contains__(self, word: str) -> bool:
        """Checks if the synonyms contain a main word."""
        return word in self._synonyms_dict

    def __getitem__(self, word: str) -> list[str]:
        """
        Get the list of synonyms for a given main word.

        :param word: The main word
        :return: The list of synonyms associated with the main word
        """
        return self._synonyms_dict.get(word, [])

    def replace(self, synonyms_dict: dict[str, list[str]]) -> None:
        """
        Replace the synonyms with the provided mapping.

        :param synonyms_dict: A dictionary where keys represent main words and values represent synonyms.
        :return: None
        """
        self._synonyms_dict = synonyms_dict.copy()



"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University 
(Department of Information and Computing Sciences)
"""
