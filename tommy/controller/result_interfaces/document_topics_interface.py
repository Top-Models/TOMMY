from abc import ABC, abstractmethod
from collections.abc import Iterable

from numpy import ndarray


class DocumentTopicsInterface(ABC):
    """
    Abstract class that defines the interface for getting
    a distribution of topics in a given preprocessed document
    """

    @abstractmethod
    def get_document_topics(self, doc: list[str],
                            minimum_probability: float) -> ndarray:
        """
        Returns the topic distribution for the given preprocessed document
        as a list of (topic_id, topic_probability) tuples
        :param doc: the list of terms of a document
        :param minimum_probability: the minimum probability of a topic for
            it to be included in the results
        :return: a two-dimensional numpy array which can be read as a list of
            (topic_id, topic_probability) pairs
        """


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University 
(Department of Information and Computing Sciences)
"""
