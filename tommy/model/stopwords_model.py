import os
from collections.abc import Iterable


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
        with open(os.path.join("backend", "preprocessing", "stopwords.txt"),
                  'r') as file:
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
        # Only 1 argument and it's a list or tuple.
        if len(args) == 1 and isinstance(args[0], Iterable):
            words = args[0]
        # Otherwise the arguments should be the words themselves.
        else:
            words = args
        # Add the words to the set.
        for word in words:
            self._extra_words.add(word)

    def remove(self, *args: str | Iterable[str]) -> None:
        """
        Remove one or more extra stopwords.

        :param args: The word(s) to remove from the iterable
        :return: None
        """
        # Only 1 argument and it's a list or tuple.
        if len(args) == 1 and isinstance(args[0], Iterable):
            words = args[0]
        # Otherwise the arguments should be the words themselves.
        else:
            words = args
        # Remove the words from the set.
        for word in words:
            self._extra_words.discard(word)

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
