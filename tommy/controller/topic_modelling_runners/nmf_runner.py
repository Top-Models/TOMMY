from collections.abc import Iterable

from numpy import ndarray
from gensim.corpora.dictionary import Dictionary
from gensim.models.nmf import Nmf

from tommy.model.topic_model import TopicModel
from tommy.datatypes.topics import Topic, TopicWithScores
from tommy.controller.result_interfaces.correlation_matrix_interface import (
    CorrelationMatrixInterface)
from tommy.controller.result_interfaces.document_topics_interface import (
    DocumentTopicsInterface)

from tommy.controller.topic_modelling_runners.abstract_topic_runner import (
    TopicRunner)

STANDARD_RANDOM_SEED = 42


class NMFRunner(TopicRunner,
                DocumentTopicsInterface):
    """GensimNMF class for topic modeling using NMF with Gensim."""
    _num_topics: int
    _random_seed: int

    @property
    def _dictionary(self) -> Dictionary:
        """get the term_ids-to-terms dictionary saved in the topic model"""
        return self._topic_model.model['dictionary']

    @_dictionary.setter
    def _dictionary(self, new_dictionary: Dictionary) -> None:
        """Takes and sets the term_ids-to-terms dictionary"""
        self._topic_model.model['dictionary'] = new_dictionary

    @property
    def _model(self) -> Nmf:
        """Get the model than is being run from the topic model"""
        return self._topic_model.model['model']

    @_model.setter
    def _model(self, new_model: Nmf) -> None:
        """Set the LDA model than is being run in the topic model"""
        self._topic_model.model['model'] = new_model

    def __init__(self, topic_model: TopicModel, docs: Iterable[list[str]],
                 num_topics: int, random_seed=STANDARD_RANDOM_SEED) -> None:
        """
        Initialize the GensimLdaModel.
        :param topic_model: Reference to the topic model where the algorithm
            and data should be saved.
        :param docs: Generator returning the preprocessed lists of words as
            training input
        :param num_topics: Number of topics to the model.
        :param random_seed: Seed for reproducibility, defaults to 42.
        :return: None
        """
        super().__init__(topic_model=topic_model)

        # clear location where model and dictionary will be stored
        self._topic_model.model = {}

        self._num_topics = num_topics
        self._random_seed = random_seed
        self.train_model(docs)

    def train_model(self, docs: Iterable[list[str]]) -> None:
        """
        Train the LDA model on the given documents and save the resulting model
        and dictionary in the topic model ready to return results.
        :param docs: Generator returning the preprocessed lists of words as
            training input
        :return: None
        """

        self._dictionary = Dictionary(docs)
        bags_of_words = [self._dictionary.doc2bow(tokens)
                         for tokens in docs]
        self._model = Nmf(corpus=bags_of_words,
                          id2word=self._dictionary,
                          num_topics=self._num_topics,
                          random_state=self._random_seed)

    def get_n_topics(self) -> int:
        return self._num_topics

    def get_topic_with_scores(self, topic_id,
                              n_words) -> TopicWithScores:
        words_with_scores = self._model.show_topic(topicid=topic_id,
                                                   topn=n_words)
        return TopicWithScores(topic_id, words_with_scores)

    def get_topics_with_scores(self, n_words) -> list[TopicWithScores]:
        # Underlying library in gensim has a bug where it crashes when
        # n_words is 0. This is a workaround.
        if n_words == 0:
            return [TopicWithScores(topic_id, [])
                    for (topic_id, _)
                    in
                    self._model.show_topics(formatted=False,
                                            num_words=1,
                                            num_topics=self._num_topics)]
        return [TopicWithScores(topic_id, words_with_scores)
                for (topic_id, words_with_scores)
                in self._model.show_topics(formatted=False,
                                           num_words=n_words,
                                           num_topics=self._num_topics)]

    def get_document_topics(self, doc, minimum_probability):
        bag_of_words = self._dictionary.doc2bow(doc)
        return self._model.get_document_topics(bag_of_words,
                                               minimum_probability=
                                               minimum_probability)


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University 
(Department of Information and Computing Sciences)
"""
