from collections.abc import Iterable

from gensim.corpora.dictionary import Dictionary
from gensim.models.ldamodel import LdaModel
from numpy import ndarray

from tommy.controller.result_interfaces.correlation_matrix_interface import (
    CorrelationMatrixInterface)
from tommy.controller.result_interfaces.document_topics_interface import (
    DocumentTopicsInterface)
from tommy.controller.topic_modelling_runners.abstract_topic_runner import (
    TopicRunner)
from tommy.datatypes.topics import TopicWithScores
from tommy.model.topic_model import TopicModel

STANDARD_RANDOM_SEED = 42


class LdaRunner(TopicRunner,
                CorrelationMatrixInterface,
                DocumentTopicsInterface):
    """GensimLdaModel class for topic modeling using LDA with Gensim."""
    _num_topics: int
    _alpha: float
    _beta: float
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
    def _model(self) -> LdaModel:
        """Get the model than is being run from the topic model"""
        return self._topic_model.model['model']

    @_model.setter
    def _model(self, new_model: LdaModel) -> None:
        """Set the LDA model than is being run in the topic model"""
        self._topic_model.model['model'] = new_model

    def __init__(self,
                 topic_model: TopicModel,
                 docs: Iterable[list[str]],
                 num_topics: int,
                 alpha: float = None,
                 beta: float = None,
                 random_seed=STANDARD_RANDOM_SEED) -> None:
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
        self._alpha = alpha
        self._beta = beta
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

        # Run optimized LDA if alpha and beta are None
        if self._alpha and self._beta is None:
            self._model = LdaModel(corpus=bags_of_words,
                                   id2word=self._dictionary,
                                   num_topics=self._num_topics,
                                   random_state=self._random_seed)
            return

        # Run LDA with custom alpha and beta
        self._model = LdaModel(corpus=bags_of_words,
                               id2word=self._dictionary,
                               num_topics=self._num_topics,
                               random_state=self._random_seed,
                               alpha=self._alpha,
                               eta=self._beta)

    def get_n_topics(self) -> int:
        return self._num_topics

    def get_topic_with_scores(self, topic_id,
                              n_words) -> TopicWithScores:
        words_with_scores = self._model.show_topic(topicid=topic_id,
                                                   topn=n_words)
        return TopicWithScores(topic_id, words_with_scores)

    def get_topics_with_scores(self, n_words) -> list[TopicWithScores]:
        return [TopicWithScores(topic_id, words_with_scores)
                for (topic_id, words_with_scores)
                in self._model.show_topics(formatted=False, num_words=n_words)]

    def get_correlation_matrix(self, n_words_to_process: int) -> ndarray:
        """
        Get the array of distances (in the sense of similarity) between
        different topics in the model.
        :param n_words_to_process: The number of to take into account when
            calculating the distance between topics.
        :return: n_topic x n_topics matrix of floats between 0 and 1 where
            entry i,j is the distance between topic i and topic j. Entry i,j is
            close to 0 when topic i and topic j are similar and close to 1 when
            topic i and topic j are very different
        """
        return self._model.diff(self._model,
                                distance='jaccard',
                                num_words=n_words_to_process)[0]

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
