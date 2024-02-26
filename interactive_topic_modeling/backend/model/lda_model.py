from interactive_topic_modeling.backend.model.abstract_model import Model, Doc, Docs

from gensim.corpora.dictionary import Dictionary
from gensim.models.ldamodel import LdaModel

from itertools import chain

from collections.abc import Iterable
from typing import Tuple


class GensimLdaModel(Model):
    dictionary: Dictionary
    model: LdaModel
    corpus: Iterable[Iterable[Tuple[int, int]]]

    def __init__(self, docs: Docs, k: int, random_seed=None):
        super().__init__(random_seed)
        self.train_model(docs, k)

    def train_model(self, docs, k):
        self.dictionary = Dictionary(docs)
        self.corpus = [self.dictionary.doc2bow(tokens) for tokens in docs]
        self.model = LdaModel(corpus=self.corpus,
                              id2word=self.dictionary,
                              num_topics=k,
                              random_state=self.random_seed)

    def update_model(self, docs):
        added_corpus = [self.dictionary.doc2bow(tokens) for tokens in docs]
        self.model.update(added_corpus)
        self.corpus = chain(self.corpus, added_corpus)

    def get_topics(self):
        return self.model.show_topics(formatted=False)

    def get_doc_topics(self, doc):
        bag_of_words = self.dictionary.doc2bow(doc)
        return self.model[bag_of_words]
