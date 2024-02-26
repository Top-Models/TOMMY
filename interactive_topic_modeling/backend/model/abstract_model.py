# This file defines an absract base class that all topic modelling algorithms will implement
# The class will define a function to take a preprocessed input corpus
# as an iterable that yields another iterable which in turn yield the token in string format

from random import randrange

from abc import ABC, abstractmethod
from collections.abc import Iterable
from typing import Tuple, List, NewType

Doc = NewType('Doc', List[str])
Docs = NewType('Docs', Iterable[Doc])


class Model(ABC):
    _random_seed: int

    @property
    def random_seed(self):
        return self._random_seed

    @random_seed.setter
    def random_seed(self, new_random_seed: int):
        if new_random_seed is None:
            self._random_seed = randrange(1 << 16)
        elif isinstance(new_random_seed, int):
            self._random_seed = new_random_seed
        else:
            raise ValueError('Random seed passed to Model class is not an integer.', new_random_seed)

#    @abstractmethod
#    def __init__(self, docs: Docs, k: int, random_seed: int):
    def __init__(self, random_seed: int):
        self.random_seed = random_seed

    # Trains the model from scratch on the input iterable of iterables of tokens with k topics
    @abstractmethod
    def train_model(self, docs: Docs, k: int):
        pass

    # Updates the model to include the information from the input iterable of iterables of tokens
    @abstractmethod
    def update_model(self, docs: Docs):
        pass

    # Returns the found topics in the format where each topic consists of a list of
    # tuples of the word and the score of that word, e.g., [(_topid_id, [('word', 0.52), ('ortoken', 0.412)])]
    @abstractmethod
    def get_topics(self) -> List[Tuple[int, List[Tuple[str, float]]]]:
        pass

    # Returns a list with for each topic that is somewhat present in the document,
    # (the topic ID, and) the float (0 to 1) representing how much that topic is present in this document
    @abstractmethod
    def get_doc_topics(self, doc: Doc) -> list[tuple[int, float]]:
        pass
