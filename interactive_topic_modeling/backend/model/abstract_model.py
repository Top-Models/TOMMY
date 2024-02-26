# This file defines an absract base class that all topic modelling algorithms will implement
# The class will define a function to take a preprocessed input corpus, i.e., an iterable of lists of strings

from random import randrange

from abc import ABC, abstractmethod
from collections.abc import Iterable
from typing import Tuple, List, NewType
from numpy import ndarray  # todo: add numpy to project requirements
from os import path

Term = NewType('Term', str)
TermList = NewType('TermList', List[Term])
TermLists = NewType('TermLists', Iterable[TermList])


class Model(ABC):
    _num_topics: int

    @property
    def num_topics(self):
        return self._num_topics

    @num_topics.setter
    def num_topics(self, new_num_topics: int):
        if new_num_topics is None:
            return
        elif isinstance(new_num_topics, int):
            self._random_seed = new_num_topics
        else:
            raise ValueError('Number of topics passed to Model class is not an integer.', new_num_topics)

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

    def __init__(self, random_seed: int):
        self.random_seed = random_seed

    # Trains the model from scratch on the input iterable of iterables of tokens with k topics
    @abstractmethod
    def train_model(self, term_lists: TermLists, num_topics: int = None):
        pass

    # Updates the model to include the information from the input iterable of iterables of tokens
    @abstractmethod
    def update_model(self, term_lists: TermLists):
        pass

    # Returns the term that belongs to the given term_id
    @abstractmethod
    def get_term(self, term_id):
        pass

    # Returns the number of unique terms that have been received by the model
    @abstractmethod
    def n_terms(self) -> int:
        pass

    # Returns the found topics in the format where each topic consists of a list of for all top n terms the
    # tuples of the term and the score of that word, e.g., [(_topic_id, [('word', 0.52), ('etc', 0.412)])]
    @abstractmethod
    def show_topics(self, n) -> List[Tuple[int, List[Tuple[Term, float]]]]:
        pass

    # Returns the found topics in the format where each topic consists of a list of for all top n terms the
    # tuples of the term_id and the score of that word, e.g., [(_topic_id, [(42, 0.52), (58, 0.412)])]
    @abstractmethod
    def get_topics(self, n) -> List[Tuple[int, List[Tuple[int, float]]]]:
        pass

    # Returns for the topic associated with the topic_id, a list of for all top n words the
    # tuples of the word and the score of that word, e.g., [(_topic_id, [('word', 0.52), ('etc', 0.412)])]
    @abstractmethod
    def show_topic_terms(self, topic_id, n) -> List[Tuple[Term, float]]:
        pass

    # Returns for the topic associated with the topic_id, a list of for all top n terms the
    # tuples of the termID and the score of that word, e.g., [(_topic_id, [(42, 0.52), (58, 0.412)])]
    @abstractmethod
    def get_topic_terms(self, topic_id, n) -> List[Tuple[int, float]]:
        pass

    # Returns a list with for each topic that is at least with minimum_probability present in the document,
    # (the topic ID, and) the float (0 to 1) representing how much that topic is present in this document
    @abstractmethod
    def get_doc_topics(self, term_list: TermList, minimum_probability=0) -> list[tuple[int, float]]:
        pass

    # Returns a numpy array of size n_topics x n_terms, where the values represent the probability for each
    # term in each topic.
    @abstractmethod
    def get_topic_term_numpy_matrix(self) -> ndarray:
        pass

    # Saves the internal state of the model to the location on the hard disk specified by fpath
    @abstractmethod
    def save(self, fpath: path):
        pass

    # Loads a Model from an earlier saved internal state. This method returns an instance of the Model.
    # So use for example: "my_lda_model = GensimLdaModel.load(os.curdir)"
    @classmethod
    @abstractmethod
    def load(cls, fpath: path):
        pass
