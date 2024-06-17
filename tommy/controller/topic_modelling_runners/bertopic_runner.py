import string

from numpy import ndarray
from sklearn.feature_extraction.text import CountVectorizer
from bertopic import BERTopic
from bertopic.vectorizers import ClassTfidfTransformer

from tommy.controller.stopwords_controller import StopwordsController
from tommy.controller.corpus_controller import RawFile
from tommy.datatypes.topics import TopicWithScores
from tommy.model.topic_model import TopicModel
from tommy.controller.topic_modelling_runners.abstract_topic_runner import (
    TopicRunner)


class BertopicRunner(TopicRunner):
    """
    BertopicRunner class for running the BERTopic topic modelling algorithm.
    """

    @property
    def _model(self) -> BERTopic:
        """get the bertopic model object saved in the topic_model"""
        return self._topic_model.model['model']

    @_model.setter
    def _model(self, new_model: BERTopic) -> None:
        """set the bertopic model object in the topic_model"""
        self._topic_model.model['model'] = new_model

    @property
    def num_words_per_topic(self) -> int:
        """the number of words that are calculated per topic"""
        return self._topic_model.model['num_words_per_topic']

    @property
    def max_num_topics(self) -> int:
        """the maximum number of topics that are calculated per topic"""
        return self._topic_model.model['num_topics']

    def __init__(self, topic_model: TopicModel,
                 stopwords_controller: StopwordsController,
                 current_corpus_version_id: int,
                 num_topics: int,
                 num_words_per_topic: int,
                 docs: list[str],
                 sentences: list[str],
                 min_df: float | None,
                 max_features: int | None) -> None:
        """
        Initialize the BertopicRunner.
        :param topic_model: reference to the topic model where the algorithm
            and data should be saved
        :param stopwords_controller: a reference to the stopwords controller to
            extract the stopwords from
        :param current_corpus_version_id: The version identifier of the corpus
            that is used in training
        :param num_topics: the MAXIMUM number of topics to be returned from
            the analysis
        :param num_words_per_topic: the number of words per topic to be
            calculated. Values between 10-20 advised due to computation time.
        :param min_df: The minimal document frequency for a term to be
            included. I.E., the minimal ratio of the sentences in which te term
            needs to occur
        :param max_features: The maximum number of terms to be included in the
            analysis
        :return: None
        """
        super().__init__(topic_model, current_corpus_version_id)
        self._stopwords_controller = stopwords_controller

        self._topic_model.model = {}
        self._topic_model.model['num_words_per_topic'] = num_words_per_topic
        self._topic_model.model['num_topics'] = num_topics

        self.train_model(docs, sentences,
                         min_df=min_df,
                         max_features=max_features)

    def get_n_topics(self) -> int:
        """Returns the number of topics calculated by the model."""
        return len([... for topic_words
                    in self._model.get_topics().values()
                    if topic_words])

    def get_model(self) -> string:
        return "BERTOPIC"

    def get_topic_with_scores(self, topic_id: int, n_words: int):
        """
        Return a topic object containing top n terms and their corresponding
        score for the topic identified by the topic_index.
        :param topic_id: the index of the requested topic
        :param n_words: number of terms in the resulting topic object,
            Note: BERTopic does not support top n queries
        :return: topic object containing top n terms and their corresponding
            scores
        """
        topics = [topic_words for topic_words
                  in self._model.get_topics().values()
                  if topic_words]

        # type hint in BERTopic's get_topics() function is incorrect
        # noinspection PyTypeChecker
        return TopicWithScores(topic_id, topics[topic_id])

    def get_topics_with_scores(self, n_words: int):
        """
        Return a list of topic objects containing top n terms and their
        corresponding scores.
        :param n_words: number of terms in the resulting topic objects,
            Note: BERTopic does not support top n queries
        :return: list of topic objects containing the top n terms and their
            corresponding scores
        """
        # type hint in BERTopic's get_topics() function is incorrect
        # noinspection PyTypeChecker
        return [TopicWithScores(topic_id=topic_id,
                                top_words_with_scores=topic_words)
                for topic_id, topic_words
                in enumerate(self._model.get_topics().values())
                if topic_words]

    def train_model(self, docs: list[str], sentences: list[str],
                    min_df: float | None,
                    max_features: int | None) -> None:
        """
        Train the BERTopic model.
        :param docs: list containing the raw bodies of files as
            input data
        :param sentences: list containing the raw bodies of files split into
            sentences as training input
        :param min_df: The minimal document frequency for a term to be
            included. I.E., the minimal ratio of the sentences in which te term
            needs to occur
        :param max_features: The maximum number of terms to be included in the
            analysis
        :return: None
        """
        hyperparams = {}
        if min_df is not None:
            hyperparams['min_df'] = min_df
        if max_features is not None:
            hyperparams['max_features'] = max_features

        vectorizer_model = CountVectorizer(
            ngram_range=(1, 3),
            stop_words=list(stopword for stopword
                            in self._stopwords_controller.stopwords_model),
            **hyperparams)
        ctfidf_model = ClassTfidfTransformer(reduce_frequent_words=True)
        self._model = BERTopic(
            vectorizer_model=vectorizer_model, ctfidf_model=ctfidf_model,
            top_n_words=self.num_words_per_topic, nr_topics=self.max_num_topics
        ).fit(sentences)


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University
(Department of Information and Computing Sciences)
"""
