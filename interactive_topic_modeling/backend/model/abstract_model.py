# This file defines an absract base class that all topic modelling algorithms will implement
# The class will define a function to take a preprocessed input corpus, i.e., an iterable of lists of strings

from random import randrange

from abc import ABC, abstractmethod
from collections.abc import Iterable
from typing import Tuple, List, TypeAlias, Dict
from numpy import ndarray
from os import path

TermList: TypeAlias = List[str]
TermLists: TypeAlias = Iterable[TermList]


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
            self._num_topics = new_num_topics
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
        self._num_topics = 10
        self.random_seed = random_seed

    @abstractmethod
    def train_model(self, term_lists: TermLists, num_topics: int = None, **parameters: Dict[str, any]):
        """Trains the model from scratch on the input iterable of iterables of terms

        Keyword arguments:
        num_topics -- the number of topics that the topic modelling should result in (default: the last used num_topics)
        [See https://radimrehurek.com/gensim/models/ldamodel.html#gensim.models.ldamodel.LdaModel for documentation
        on the rest of the keyword arguments]
        """
        pass

    @abstractmethod
    def update_model(self, term_lists: TermLists, **parameters: Dict[str, any]):
        """Updates the model to include the information from the input iterable of iterables of tokens

        Keywords arguments:
        [See https://radimrehurek.com/gensim/models/ldamodel.html#gensim.models.ldamodel.LdaModel.update]
        """
        pass

    @abstractmethod
    def get_term(self, term_id: int) -> str:
        """Returns the term that belongs to the given term_id"""
        pass

    @abstractmethod
    def n_terms(self) -> int:
        """Returns the number of unique terms that have been received by the model"""
        pass

    @abstractmethod
    def show_topics(self, n: int) -> List[Tuple[int, List[Tuple[str, float]]]]:
        """returns for all topics the topic_id and the n best terms with their scores, e.g.:
        [(topic_id, [(term1, term1_probability), (term2, term2_probability), etc.]), etc.]
        """
        pass

    @abstractmethod
    def get_topics(self, n: int) -> List[Tuple[int, List[Tuple[int, float]]]]:
        """returns for all topics the topic_id and the term_id and the scores of the n best terms, e.g.:
        [(topic_id, [(term_id1, term1_probability), (term_id2, term2_probability), etc.]), etc.]
        """
        pass

    @abstractmethod
    def show_topic_terms(self, topic_id: int, n: int) -> List[Tuple[str, float]]:
        """returns for the topic identified by topic_id the n best terms with their scores, e.g.:
        [(term1, term1_probability), (term2, term2_probability), etc.]
        """
        pass

    @abstractmethod
    def get_topic_terms(self, topic_id: int, n: int) -> List[Tuple[int, float]]:
        """returns for the topic identified by topic_id the term_ids and scores of the n best terms, e.g.:
        [(term_id1, term1_probability), (term_id2, term2_probability), etc.]
        """
        pass

    @abstractmethod
    def get_doc_topics(self, term_list: TermList, minimum_probability=0) -> list[tuple[int, float]]:
        """Analyzes the document represented by the term_list to return the topic_id and probability
        of all topics in the document, e.g.: [(topic_id1, topic1_probability), (topic_id2, topic2_probability), etc.]

        Keyword arguments:
        minimum_probability -- the minimum probability score that a topic needs for it to be included in the results
        """
        pass

    @abstractmethod
    def show_topic(self, topic_id: int, n: int) -> list[tuple[str, float]]:
        """"Returns the top n probability pairs where words are actual strings for the current topic_id"""
        pass

    @abstractmethod
    def show_topic_and_probs(self, topic_id: int, n: int) -> tuple[list[str], list[float]]:
        """"Return the top n words represented as strings and their associated probabilities in two separate lists"""
        pass

    @abstractmethod
    def get_topic_term_numpy_matrix(self) -> ndarray:
        """Returns the n_topics x n_terms numpy array of calculated probabilities of each combination of topics and terms
        i.e.: "my_model.get_topic_term_numpy_matrix()[my_topic_id, my_term_id]"
        """
        pass

    @abstractmethod
    def get_correlation_matrix(self, num_words: int) -> ndarray:
        """Returns the n_topics x n_topics array of similarities between different topics of the same LDA model"""
        pass

    @abstractmethod
    def save(self, fpath: path):
        """Saves the internal state of the model to the location on the hard disk specified by fpath"""
        pass

    @classmethod
    @abstractmethod
    def load(cls, fpath: path):
        """Loads a Model from an earlier saved internal state. This method returns an instance of the Model.
        e.g.: "my_lda_model = GensimLdaModel.load(os.curdir)"
        """
        pass
