from __future__ import annotations


class SynonymsModel:
    """
    A class representing the dictionary of synonyms.

    The class acts as a wrapper around a dictionary of synoyms, providing basic
    map-like functionality. This model can be used to map source words to
    target words (synonyms).
    """

    @property
    def synonyms(self) -> dict[str, str]:
        return self._synonyms

    def __init__(self, derive_from: SynonymsModel = None) -> None:
        """Initializes the synonyms model."""
        if derive_from is None:
            self._synonyms = dict()
        else:
            self._synonyms = derive_from.synonyms.copy()

    def __len__(self) -> int:
        """Gets the number of synonyms."""
        return len(self._synonyms)

    def __contains__(self, word: str) -> bool:
        """Checks if the dictionary of synonyms contains a source word."""
        return word in self._synonyms

    def __setitem__(self, key: str, item: str):
        """Adds a synonym to the dictionary."""
        self._synonyms[key] = item

    def __getitem__(self, key: str):
        """Gets the synonym for a given source word"""
        return self._synonyms[key]

    def get(self, key: str, default: str = None) -> str:
        """
        Gets the synonym for a given source word.
        Returns a default value when the source word is not found.

        :param key: The source word
        :param default: The default value to return
        if the source word is not found, defaults to None
        :return: The synonym associated with the source word
        """
        return self._synonyms.get(key, default)

    def replace(self, synonyms: dict[str, str]) -> None:
        """
        Replace the synonyms with the provided mapping.

        :param synonyms: A dictionary where the keys represent source words
        and the values represent target words.
        :return: None
        """
        self._synonyms = synonyms

    def to_dict(self) -> dict[str, str]:
        """
        Convert the synonyms model to a dictionary.

        :return: Dictionary representation of the synonyms model
        """
        return self._synonyms

    @classmethod
    def from_dict(cls, synonyms_dict: dict[str, str]) -> SynonymsModel:
        """
        Create a SynonymsModel instance from a dictionary representation.

        :param synonyms_dict: Dictionary representation of the synonyms model
        :return: SynonymsModel instance
        """
        synonyms = cls()
        synonyms.replace(synonyms_dict)

        # check that every value is of type string
        for key, value in synonyms_dict.items():
            if not isinstance(value, str):
                raise TypeError(f"Synonyms should be strings, but they are "
                                f"not. The value for key {key} is {value}.")

        return synonyms


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University
(Department of Information and Computing Sciences)
"""
