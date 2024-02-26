from interactive_topic_modeling.backend.model.abstract_model import Model, TermLists

from gensim.corpora.dictionary import Dictionary
from gensim.models.ldamodel import LdaModel

from itertools import chain

from collections.abc import Iterable
from typing import Tuple


class GensimLdaModel(Model):
    dictionary: Dictionary
    model: LdaModel
    bags_of_words: Iterable[Iterable[Tuple[int, int]]]

    def __init__(self, term_lists: TermLists, num_topics: int, random_seed=None):
        super().__init__(random_seed)
        self.num_topics = num_topics
        self.train_model(term_lists)

    def train_model(self, docs, num_topics=None):
        self.num_topics = num_topics

        self.dictionary = Dictionary(docs)
        self.bags_of_words = [self.dictionary.doc2bow(tokens) for tokens in docs]
        self.model = LdaModel(corpus=self.bags_of_words,
                              id2word=self.dictionary,
                              num_topics=num_topics,
                              random_state=self.random_seed)

    def update_model(self, docs):
        added_corpus = [self.dictionary.doc2bow(tokens) for tokens in docs]
        self.model.update(added_corpus)
        self.bags_of_words = chain(self.bags_of_words, added_corpus)

    def get_term(self, term_id):
        return self.dictionary[term_id]

    def n_terms(self):
        return len(self.dictionary)

    def show_topics(self, n):
        return self.model.show_topics(formatted=False, num_words=n)

    def get_topics(self, n):
        return [(topic_id, ) for topic_id in range(self.num_topics)]

    def show_topic_terms(self, topic_id, n):
        return self.model.show_topic(topic_id, topn=n)

    def get_topic_terms(self, topic_id, n):
        return self.model.get_topic_terms(topic_id, topn=n)

    def get_doc_topics(self, doc, minimum_probability=0):
        bag_of_words = self.dictionary.doc2bow(doc)
        return self.model.get_document_topics(bag_of_words, minimum_probability=minimum_probability)

    def get_topic_term_numpy_matrix(self):
        return self.model.get_topics()

    def save(self, fpath):
        raise NotImplementedError("Saving the model has not been implemented in GensimLdaModel")

    @classmethod
    def load(cls, fpath):
        raise NotImplementedError("Loading the model has not been implemented in GensimLdaModel")
