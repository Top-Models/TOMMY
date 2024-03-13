from random import randrange
from abc import ABC, abstractmethod
from collections.abc import Iterable
from typing import Tuple, List, Dict
from numpy import ndarray
from os import path

TermList = List[str]
TermLists = Iterable[TermList]


class Model(ABC):
    """
    This abstract base class defines the interface that all topic modelling
    algorithms will implement.
    """

    _num_topics: int
    _random_seed: int

    @property
    def num_topics(self) -> int:
        """
        Number of topics in the model.
        """
        return self._num_topics

    @num_topics.setter
    def num_topics(self, new_num_topics: int):
        """
        Set the number of topics.
        """
        if new_num_topics is None:
            return
        elif isinstance(new_num_topics, int):
            self._num_topics = new_num_topics
        else:
            raise ValueError("Number of topics passed to "
                             "Model class is not an integer.",
                             new_num_topics)

    @property
    def random_seed(self) -> int:
        """The seed used for the model."""
        return self._random_seed

    @random_seed.setter
    def random_seed(self, new_random_seed: int) -> None:
        """Set a new 'random' seed."""
        if new_random_seed is None:
            self._random_seed = randrange(1 << 16)
        elif isinstance(new_random_seed, int):
            self._random_seed = new_random_seed
        else:
            raise ValueError("Random seed passed to Model class is "
                             "not an integer.",
                             new_random_seed)

    def __init__(self, random_seed: int) -> None:
        """Initialization of the AbstractModel object."""
        self._num_topics = 10
        self.random_seed = random_seed

    @abstractmethod
    def train_model(self,
                    term_lists: TermLists,
                    num_topics: int = None,
                    **parameters: Dict[str, any]) -> None:
        """
        Trains the model from scratch on the input iterable of iterables
        of terms.

        :param term_lists: The input corpus.
        :param num_topics: Number of topics. Default is None.
        :param parameters: Additional parameters.

        :return NotImplementedError: If the method is not implemented.
        """
        pass

    @abstractmethod
    def update_model(self,
                     term_lists: TermLists,
                     **parameters: Dict[str, any]) -> None:
        """
        Updates the model to include the information from the input iterable
        of iterables of tokens.

        :param term_lists: The input corpus.
        :param parameters: Additional parameters.
        """
        pass

    @abstractmethod
    def get_term(self, term_id: int) -> str:
        """Returns the term that belongs to the given term_id"""
        pass

    @abstractmethod
    def n_terms(self) -> int:
        """
        Returns the number of unique terms that have been
        received by the model
        """
        pass

    @abstractmethod
    def show_topics(self, n: int) -> List[Tuple[int, List[Tuple[str, float]]]]:
        """
        Returns the top n terms for each topic.

        :param n: Number of terms to return per topic.
        :return List[Tuple[int, List[Tuple[str, float]]]]: List of tuples
                containing topic ID and its top terms.
        """
        pass

    @abstractmethod
    def get_topics(self, n: int) -> List[Tuple[int, List[Tuple[int, float]]]]:
        """
        Returns the top n terms with their probabilities for each topic.

        :param n: Number of terms to return per topic.
        :return List[Tuple[int, List[Tuple[int, float]]]]:
        List of tuples containing topic ID and its top term IDs
        with probabilities.
        """
        pass

    @abstractmethod
    def show_topic_terms(self, topic_id: int, n: int) -> List[Tuple[str,
                                                                    float]]:
        """
        Returns the top n terms for a specific topic.

        :param topic_id: ID of the topic.
        :param n: Number of terms to return.
        :return: [Tuple[str, float]]: List of tuples containing term
                                      and its probability.
        """
        pass

    @abstractmethod
    def get_topic_terms(self, topic_id: int, n: int) -> List[Tuple[int,
                                                                   float]]:
        """
        Returns the top n term IDs with their probabilities for a
        specific topic.

        :param topic_id: ID of the topic.
        :param n: Number of terms to return.
        :return [Tuple[int, float]]: List of tuples containing term ID
                                     and its probability.
        """
        pass

    @abstractmethod
    def get_doc_topics(self, term_list: TermList, minimum_probability=0) -> (
                       list)[tuple[int, float]]:
        """
        Analyzes the document represented by the term_list to return
        the topic_id and probability of all topics in the document.


        :param term_list: List of terms representing the document.
        :param minimum_probability: Minimum probability score for a topic
                                    to be included in the results.
        :return [Tuple[int, float]]: List of tuples containing topic ID
                                     and its probability.
        """
        pass

    @abstractmethod
    def show_topic(self, topic_id: int, n: int) -> list[tuple[str, float]]:
        """
        Returns the top n probability pairs where words are actual strings
        for the current topic_id.

        :param topic_id: ID of the topic.
        :param n: Number of terms to return.
        :return [Tuple[str, float]]: List of tuples containing term
                                     and its probability.
        """
        pass

    @abstractmethod
    def show_topic_and_probs(self, topic_id: int, n: int) -> (
                             tuple)[list[str], list[float]]:
        """
        Return the top n words represented as strings and their
        associated probabilities in two separate lists.

        :param topic_id: ID of the topic.
        :param n: Number of terms to return.
        :return Tuple[List[str], List[float]]: Tuple containing two lists
                                               list of terms
                                               and list of probabilities.
        """
        pass

    @abstractmethod
    def get_topic_term_numpy_matrix(self) -> ndarray:
        """
        Returns the n_topics x n_terms numpy array of calculated
        probabilities of each combination of topics and terms.

        :return ndarray: Numpy array containing probabilities.
        """
        pass

    @abstractmethod
    def get_correlation_matrix(self, num_words: int) -> ndarray:
        """
        Returns the n_topics x n_topics array of similarities
        between different topics of the same LDA model.

        :param num_words: Number of words to consider for similarity
                          calculation.
        :return ndarray: Numpy array containing similarity scores.
        """
        pass

    @abstractmethod
    def save(self, fpath: path) -> None:
        """
        Saves the internal state of the model to the location on
        the hard disk specified by fpath
        """
        pass

    @classmethod
    @abstractmethod
    def load(cls, fpath: path) -> "Model":
        """
        Loads a Model from an earlier saved internal state.

        :param fpath: File path.
        :return Model: Loaded model instance.
        """
        pass
