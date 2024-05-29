import numpy as np

from collections.abc import Iterable
from numpy import ndarray

from gensim.corpora.dictionary import Dictionary
from gensim.models.nmf import Nmf
from gensim.models.coherencemodel import CoherenceModel

from tommy.controller.file_import.processed_corpus import ProcessedCorpus
from tommy.model.topic_model import TopicModel
from tommy.datatypes.topics import TopicWithScores
from tommy.controller.result_interfaces.correlation_matrix_interface import (
    CorrelationMatrixInterface)
from tommy.controller.result_interfaces.document_topics_interface import (
    DocumentTopicsInterface)
from tommy.controller.result_interfaces.topic_coherence_interface import (
    TopicCoherenceInterface)
from tommy.controller.topic_modelling_runners.abstract_topic_runner import (
    TopicRunner)

STANDARD_RANDOM_SEED = 42


class NmfRunner(TopicRunner,
                DocumentTopicsInterface,
                CorrelationMatrixInterface,
                TopicCoherenceInterface):
    """GensimNMF class for topic modeling using NMF with Gensim."""
    _num_topics: int
    _random_seed: int

    @property
    def _dictionary(self) -> Dictionary:
        """get the term_ids-to-terms dictionary saved in the topic model"""
        return self._topic_model.dictionary

    @_dictionary.setter
    def _dictionary(self, new_dictionary: Dictionary) -> None:
        """Takes and sets the term_ids-to-terms dictionary"""
        self._topic_model.dictionary = new_dictionary

    @property
    def _model(self) -> Nmf:
        """Get the model than is being run from the topic model"""
        return self._topic_model.model
    
    @_model.setter
    def _model(self, new_model: Nmf) -> None:
        """Set the NMF model than is being run in the topic model"""
        self._topic_model.model = new_model

    @property
    def _bags_of_words(self) -> list[list[tuple[int, int]]]:
        """Get the bags of words for the topic model"""
        return self._topic_model.corpus

    @_bags_of_words.setter
    def _bags_of_words(self, bag: list[list[tuple[int, int]]]) -> None:
        """Set the bags of words"""
        self._topic_model.corpus = bag

    def __init__(self, topic_model: TopicModel,
                 processed_corpus: ProcessedCorpus,
                 current_corpus_version_id: int,
                 num_topics: int,
                 random_seed=STANDARD_RANDOM_SEED) -> None:
        """
        Initialize the GensimNmfModel.
        :param topic_model: Reference to the topic model where the algorithm
            and data should be saved.
        :param processed_corpus: The processed corpus
        :param current_corpus_version_id: The version identifier of the corpus
            that is used in training
        :param num_topics: Number of topics to the model.
        :param random_seed: Seed for reproducibility, defaults to 42.
        :return: None
        """
        super().__init__(topic_model, current_corpus_version_id)

        self._num_topics = num_topics
        self._random_seed = random_seed
        self.train_model(processed_corpus)
        self.calculate_document_topics(processed_corpus, topic_model)

    def train_model(self, processed_corpus: ProcessedCorpus) -> None:
        """
        Train the NMF model on the given documents and save the resulting model
        and dictionary in the topic model ready to return results.
        :param processed_corpus: The processed corpus
        :return: None
        """

        processed_bodies = [document.body.body for document in processed_corpus]

        self._dictionary = Dictionary(processed_bodies)
        bags_of_words = [self._dictionary.doc2bow(tokens)
                         for tokens in processed_bodies]
        self._bags_of_words = bags_of_words

        self._model = Nmf(corpus=bags_of_words,
                          id2word=self._dictionary,
                          num_topics=self._num_topics,
                          random_state=self._random_seed)

    def calculate_document_topics(self,
                                  processed_corpus: ProcessedCorpus,
                                  topic_model: TopicModel) -> None:

        topic_model.document_topics = []
        n_topics = self.get_n_topics()

        for document in processed_corpus:
            topic_correspondence = (
                self.get_document_topics(document.body.body, 0.0))

            if len(topic_correspondence) != n_topics:
                print(f"Document {document.metadata.name} has "
                      f"{len(topic_correspondence)} topics "
                      f"instead of {n_topics}")

            probabilities = [0.0] * n_topics

            # Create list of topic probabilities for each document
            for (topic_id, topic_probability) in topic_correspondence:
                probabilities[topic_id] = topic_probability

            topic_model.document_topics.append(
                (document.metadata, probabilities))

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
                in self._model.show_topics(formatted=False,
                                           num_words=n_words,
                                           num_topics=self._num_topics)]

    def get_document_topics(self, doc, minimum_probability):
        bag_of_words = self._dictionary.doc2bow(doc)
        return self._model.get_document_topics(bag_of_words,
                                               minimum_probability=
                                               minimum_probability)

    def get_correlation_matrix(self, **kwargs) -> ndarray:
        """
        Calculate the topic correlation matrix.

        :return: ndarray representing the correlation matrix of topics.
        """
        topic_word_distribution = self._model.get_topics()

        # Binarize the topic-word distribution based on a set threshold 0.01
        # i.e. see if a word is related enough to a topic
        binary_topic_distribution = (topic_word_distribution >
                                     0.005).astype(int)

        num_topics = binary_topic_distribution.shape[0]
        dice_matrix = np.zeros((num_topics, num_topics))

        # Compute the Dice-Sørensen coefficient for each pair of topics
        for i in range(num_topics):
            for j in range(num_topics):
                # Check if intersection is 1 or 0
                intersection = np.sum(
                    binary_topic_distribution[i] *
                    binary_topic_distribution[j])

                sum_i = np.sum(binary_topic_distribution[i])
                sum_j = np.sum(binary_topic_distribution[j])

                # Fill in the formula
                if sum_i + sum_j > 0:
                    dice_matrix[i, j] = 2 * intersection / (
                                sum_i + sum_j)
                # Dividing by zero is impossible, so make it 0
                else:
                    dice_matrix[i, j] = 0.0

        return dice_matrix

    def get_topic_coherence(self, num_topics):
        new_model = Nmf(corpus=self._bags_of_words,
                        id2word=self._dictionary,
                        num_topics=num_topics,
                        random_state=self._random_seed)

        coherence_model = CoherenceModel(model=new_model,
                                         corpus=self._bags_of_words,
                                         dictionary=self._dictionary,
                                         coherence="u_mass")
        coherence = coherence_model.get_coherence()
        return coherence


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University 
(Department of Information and Computing Sciences)
"""
