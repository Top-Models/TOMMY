from abc import ABC, abstractmethod


class TopicCoherenceInterface(ABC):
    """
    Abstract class that defines the interface for getting a coherence value for
    an amount of topics
    """

    @abstractmethod
    def get_topic_coherence(self, num_topics: int) -> float:
        """
        Returns the topic coherence value for the given amount of topics
        :param num_topics: The number of topics
        :return: the topic coherence value
        """


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University
(Department of Information and Computing Sciences)
"""