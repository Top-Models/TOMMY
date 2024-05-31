from abc import ABC, abstractmethod

from tommy.model.topic_model import TopicModel
from tommy.datatypes.topics import Topic, TopicWithScores


class TopicRunner(ABC):
    """
    This abstract base class defines the base interface that all topic
    modelling algorithms will implement.
    """
    _topic_model: TopicModel

    @property
    def used_corpus_version_id(self) -> int | None:
        """Get the version id of the corpus that was used in the analysis"""
        return self._topic_model.used_corpus_version_id

    @used_corpus_version_id.setter
    def used_corpus_version_id(self, corpus_version_id: int) -> None:
        """set the version id of the corpus that was used in the analysis"""
        self._topic_model.used_corpus_version_id = corpus_version_id

    def __init__(self, topic_model: TopicModel,
                 used_corpus_version_id: int) -> None:
        """
        Sets the topic_model property.
        :param topic_model: reference to the topic model where data should be
            saved
        :param used_corpus_version_id: The used corpus version id
        :return: None
        """
        topic_model.document_topics = None
        topic_model.corpus = None
        self._topic_model = topic_model
        self.used_corpus_version_id = used_corpus_version_id

    @abstractmethod
    def get_n_topics(self) -> int:
        """Returns the number of topics in the model"""

    @abstractmethod
    def get_topic_with_scores(self, topic_id,
                              n_words) -> TopicWithScores:
        """
        Return a topic object containing top n terms and their corresponding
        score for the topic identified by the topic_index.

        :param topic_id: the index of the requested topic
        :param n_words: number of terms in the resulting topic object
        :return: topic object containing top n terms and their corresponding
            scores
        """

    @abstractmethod
    def get_topics_with_scores(self, n_words: int) -> list[TopicWithScores]:
        """
        Return a list of topic objects containing top n terms and their
        corresponding scores.

        :param n_words: number of terms in the resulting topic objects
        :return: list of topic objects containing the top n terms and their
            corresponding scores
        """


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University
(Department of Information and Computing Sciences)
"""
