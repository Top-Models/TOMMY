from __future__ import annotations

import os
from collections.abc import Iterable

from tommy.support.application_settings import application_settings


class StopwordsModel:
    """
    A class representing the set of stopwords.

    The class acts as a wrapper around a set of stopwords, providing basic
    iterable-like functionality. Initially it represents the set of
    basic/general stopwords imported from a text file, but extra words may
    be added, removed or replaced.
    """

    @property
    def default_words(self) -> set[str]:
        return self._default_words

    @default_words.setter
    def default_words(self, default_words: set[str]) -> None:
        self._default_words = default_words

    @property
    def extra_words(self) -> set[str]:
        return self._extra_words

    @property
    def extra_words_in_order(self) -> list[str]:
        return self._extra_words_in_order

    def __init__(self, derive_from: StopwordsModel = None) -> None:
        """Initializes the stopwords model."""
        if derive_from is None:
            self._default_words = set()
            self._extra_words = set()
            self._extra_words_in_order = []
        else:
            self._default_words = derive_from.default_words.copy()
            self._extra_words = derive_from.extra_words.copy()
            self._extra_words_in_order = (
                derive_from.extra_words_in_order.copy())

    def __len__(self) -> int:
        """Gets the number of stopwords."""
        return len(self._default_words) + len(self._extra_words)

    def __contains__(self, word: str) -> bool:
        """Checks if the set of stopwords contains a word."""
        return word in self._default_words or word in self._extra_words

    # TODO: probably deprecated
    def __iter__(self) -> Iterable[str]:
        """Returns an iterable of stopwords."""
        return iter(self._default_words | self._extra_words)

    def add(self, *args: str | Iterable[str]) -> None:
        """
        Adds one or more extra stopwords.

        :param args: The word(s) to add
        :return: None
        """
        for arg in args:
            # The argument is a string.
            if isinstance(arg, str):
                self._extra_words.add(arg)
                self._extra_words_in_order.append(arg)
            # The argument is an iterable.
            elif isinstance(arg, Iterable):
                self._extra_words.update(arg)
                self._extra_words_in_order.extend(arg)
            # The argument is of an unexpected type.
            else:
                raise TypeError(
                    "Arguments must be strings or iterables of strings.")

    def remove(self, *args: str | Iterable[str]) -> None:
        """
        Remove one or more extra stopwords.

        :param args: The word(s) to remove
        :return: None
        """
        for arg in args:
            # The argument is a string.
            if isinstance(arg, str):
                self._extra_words.discard(arg)
                self._extra_words_in_order.remove(arg)
                self._extra_words_in_order = [
                    i for i in self._extra_words_in_order if i != arg]
            # The argument is an iterable.
            elif isinstance(arg, Iterable):
                self._extra_words.difference_update(arg)
                self._extra_words_in_order = [
                    i for i in self._extra_words_in_order if i not in arg]
            # The argument is of an unexpected type.
            else:
                raise TypeError(
                    "Arguments must be strings or iterables of strings.")

    def replace(self, word_set: set[str], words_in_order: list[str]) -> None:
        """
        Replace the extra stopwords with a new set of stopwords.

        :param word_set: The new words to replace the old ones with
        :param words_in_order: The new words, but in the order that the user
        supplied them. This is necessary to make sure the order stays the same
        when switching config.
        :return: None
        """
        self._extra_words.clear()
        self._extra_words = word_set
        self._extra_words_in_order = words_in_order

    def to_dict(self) -> dict:
        """
        Convert the stopwords object to a dictionary.

        :return: Dictionary representation of the stopwords
        """
        return {
            "extra_stopwords": self._extra_words_in_order
        }

    @classmethod
    def from_dict(cls, stopwords_dict: dict) -> StopwordsModel:
        """
        Create a StopwordsModel instance from a dictionary representation.

        :param stopwords_dict: Dictionary representation of the stopwords
        :return: StopwordsModel instance
        """
        stopwords_model = cls()
        stopwords_model._extra_words_in_order = list(stopwords_dict[
                                                         "extra_stopwords"])
        stopwords_model._extra_words = set(
            stopwords_model.extra_words_in_order)
        return stopwords_model


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University
(Department of Information and Computing Sciences)
"""
