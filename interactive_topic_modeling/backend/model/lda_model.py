from gensim.corpora.dictionary import Dictionary
from gensim.models.ldamodel import LdaModel
from itertools import chain
from interactive_topic_modeling.backend.model.abstract_model import Model


class GensimLdaModel(Model):

    def __init__(self, docs, k):
        self.dictionary: Dictionary
        self.model: LdaModel
        self.train_model(docs, k)

    def train_model(self, docs, k):
        self.dictionary = Dictionary(docs)
        self.corpus = [self.dictionary.doc2bow(tokens) for tokens in docs]
        self.model = LdaModel(corpus=self.corpus, id2word=self.dictionary, num_topics=k)

    def update_model(self, docs):
        added_corpus = [self.dictionary.doc2bow(tokens) for tokens in docs]
        self.model.update(added_corpus)
        self.corpus = chain(self.corpus, added_corpus)

    def get_topics(self):
         return self.model.show_topics(formatted=False)
