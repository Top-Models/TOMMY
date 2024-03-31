import os
from collections.abc import Iterable

from tommy.support.project_settings import current_project_settings


class StopwordsModel:
    """
    A class representing the set of stopwords.

    The class acts as a wrapper around a set of stopwords, providing basic
    iterable-like functionality. Initially it represents the set of
    basic/general stopwords imported from a text file, but extra words may
    be added, removed or replaced.
    """

    def __init__(self) -> None:
        """Initializes the stopwords model."""
        with open(os.path.join(
                current_project_settings.preprocessing_data_folder,
                "stopwords.txt"), 'r') as file:
            file_content = file.read()
        stopword_list = file_content.split()
        self._default_words = set(stopword_list)

        self._extra_words = set()

    def __len__(self) -> int:
        """Gets the number of stopwords."""
        return len(self._default_words) + len(self._extra_words)

    def __contains__(self, word: str) -> bool:
        """Checks if the set of stopwords contains a word."""
        return word in self._default_words or word in self._extra_words

    def __iter__(self) -> Iterable[str]:
        """Returns an iterable of stopwords."""
        return iter(self._default_words | self._extra_words)

    def add(self, *args: str | Iterable[str]) -> None:
        """
        Adds one or more extra stopwords.

        :param args: The word(s) to add to the iterable
        :return: None
        """
        for arg in args:
            if isinstance(arg, str):
                self._extra_words.add(arg)
            elif isinstance(arg, Iterable):
                for word in arg:
                    self._extra_words.add(word)

    def remove(self, *args: str | Iterable[str]) -> None:
        """
        Remove one or more extra stopwords.

        :param args: The word(s) to remove from the iterable
        :return: None
        """
        for arg in args:
            if isinstance(arg, str):
                self._extra_words.remove(arg)
            elif isinstance(arg, Iterable):
                for word in arg:
                    self._extra_words.remove(word)

    def replace(self, *args: str | Iterable[str]) -> None:
        """
        Replace the extra stopwords with a new set of stopwords.

        :param args: The new word(s) to replace the old ones with
        :return: None
        """
        self._extra_words.clear()
        self.add(args)


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University 
(Department of Information and Computing Sciences)
"""
