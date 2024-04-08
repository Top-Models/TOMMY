from abc import ABC, abstractmethod

from numpy import ndarray


class CorrelationMatrixInterface(ABC):
    """
    Abstract class that defines the interface for getting
    a numpy correlation matrix of the similarity between topics
    """
    @abstractmethod
    def get_correlation_matrix(self, n_words_to_process: int) -> ndarray:
        """
        Get the array of distances (in the sense of similarity) between
        different topics in the model
        :param n_words_to_process: The number of to take into account when
            calculating the distance between topics; may not
            be used by every implementation.
        :return: n_topic x n_topics of floats between 0 and 1 where entry i,j
            is the distance between topic i and topic j. Entry i,j is
            close to 0 when topic i and topic j are similar and close to 1 when
            topic i and topic j are very different
        """


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University 
(Department of Information and Computing Sciences)
"""
