from numpy import ndarray
from itertools import chain
from gensim.corpora.dictionary import Dictionary
from gensim.models.ldamodel import LdaModel
from collections.abc import Iterable
from typing import Tuple, List

from interactive_topic_modeling.backend.model.abstract_model import (Model,
                                                                     TermLists)


class GensimLdaModel(Model):
    """
    GensimLdaModel class for topic modeling using LDA with Gensim.
    """

    dictionary: Dictionary
    model: LdaModel
    bags_of_words: Iterable[Iterable[Tuple[int, int]]]
    parameters: dict

    # TODO: fix random seed somewhere else
    def __init__(self, term_lists: TermLists, num_topics: int,
                 random_seed=42, **parameters):
        """
        Initialize the GensimLdaModel.
        :param term_lists: List of the term lists.
        :param num_topics: Number of topics to the model
        :param random_seed: Seed for reproducibility. Default is 42.
        :param parameters: Additional parameters for model training.
        """
        super().__init__(random_seed)
        self.parameters = {}
        self.num_topics = num_topics
        self.train_model(term_lists, **parameters)

    def train_model(self, docs, num_topics=None, **parameters) -> None:
        """
        Train the LDA model.

        :param docs: List of documents.
        :param num_topics: Number of topics
        :param parameters: Parameters to train the model
        :return: None
        """
        self.parameters.update(parameters)
        self.num_topics = num_topics

        self.dictionary = Dictionary(docs)
        self.bags_of_words = [self.dictionary.doc2bow(tokens)
                              for tokens in docs]
        self.model = LdaModel(corpus=self.bags_of_words,
                              id2word=self.dictionary,
                              num_topics=self.num_topics,
                              random_state=self.random_seed)

    def update_model(self, docs, **parameters) -> None:
        """
        Update the model with new documents.

        :param docs: List of (new) documents.
        :param parameters: Additional parameters for the model.
        :return: None
        """
        added_corpus = [self.dictionary.doc2bow(tokens) for tokens in docs]
        self.dictionary.add_documents(docs)
        self.model.update(added_corpus)
        self.bags_of_words = chain(self.bags_of_words, added_corpus)

    def get_term(self, term_id) -> str:
        """Get the term corresponding to the given id"""
        return self.dictionary[term_id]

    def n_terms(self) -> int:
        """Get the number of terms in the model"""
        return len(self.dictionary)

    def show_topics(self, n) -> List[Tuple[int, List[Tuple[str, float]]]]:
        """Show the top n terms for each topic"""
        return self.model.show_topics(formatted=False, num_words=n)

    def get_topics(self, n) -> List[Tuple[int, List[Tuple[int, float]]]]:
        """Get the top n terms with their probabilities for each topic."""
        return [(topic_id, self.get_topic_terms(topic_id, n))
                for topic_id in range(self.num_topics)]

    def show_topic_terms(self, topic_id, n) -> List[Tuple[str, float]]:
        """Show the top n terms for a specific topic"""
        return self.model.show_topic(topic_id, topn=n)

    def get_topic_terms(self, topic_id, n) -> List[Tuple[int, float]]:
        """
        Get the top n term ID's with their probabilities for a
        specific topic.

        :param topic_id: ID of the topic.
        :param n: Number of terms to return.
        :return List[Tuple[int, float]]: List of tuples containing
                                         term ID and its probability.
        """
        return self.model.get_topic_terms(topic_id, topn=n)

    def get_doc_topics(self, doc, minimum_probability=0) -> List[Tuple[int,
                                                                       float]]:
        """
        Analyse the document represented by the term_list to return the
        topic_id and probabilities of all topics in the document.

        :param doc: List of terms representing the document.
        :param minimum_probability: Minimum probability score for a topic
                                    to be included in the result
        :return: List[Tuple[int, float]]: List of tuples containing topic ID
                                          and its probability.
        """
        bag_of_words = self.dictionary.doc2bow(doc)
        return (self.model.
                get_document_topics(bag_of_words,
                                    minimum_probability=minimum_probability))

    def show_topic(self, topic_id, n) -> List[Tuple[str, float]]:
        """
        Show the top n probability pairs where words are strings for the
        current topic_id.

        :param topic_id: The id of the topic.
        :param n: Number of terms to return
        :return: List[Tuple[str, float]]: List of tuples containing term
                                          and its probability.
        """
        return self.model.show_topic(topic_id, topn=n)

    def show_topic_and_probs(self, topic_id, n) -> Tuple[List[str],
                                                         List[float]]:
        """
        Return the top n words represented as strings and their associated
        probabilities.

        :param topic_id: The ID of the topic.
        :param n: Number of terms to return.
        :return Tuple[List[str], List[float]]: Tuple containing list of words
                                               and list of probabilities.
        """
        return map(list, zip(*self.model.show_topic(topic_id, topn=n)))

    def get_topic_term_numpy_matrix(self) -> ndarray:
        """
        Get the array of calculated probabilities of each combination
        of topics and terms.
        """
        return self.model.get_topics()

    def get_correlation_matrix(self, num_words) -> ndarray:
        """
        Get the array of similarities between different topics in
        the model
        """
        return self.model.diff(self.model,
                               distance='jaccard',
                               num_words=num_words)[0]

    def save(self, fpath) -> None:
        """
        Save the internal state of the model to the location
        on the hard disk specified by fpath.
        """
        raise NotImplementedError("Saving the model has not been "
                                  "implemented in GensimLdaModel")

    @classmethod
    def load(cls, fpath) -> "Model":
        """
        Load the model from a saved internal state.
        """
        raise NotImplementedError("Loading the model has not been "
                                  "implemented in GensimLdaModel")


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University 
(Department of Information and Computing Sciences)
"""
