# This file defines an absract base class that all topic modelling algorithms will implement
# The class will define a function to take a preprocessed input corpus
# as an iterable that yields another iterable which in turn yield the token in string format

from abc import ABC, abstractmethod


class Model(ABC):

    # Trains the model from scratch on the input iterable of iterables of tokens with k topic
    @abstractmethod
    def train_model(self, docs, k):
        pass

    # Updates the model to include the information from the input iterable of iterables of tokens
    @abstractmethod
    def update_model(self, docs):
        pass

    # Will return the found topics in the format where each topic consists of a list of
    # tuples of the word and the score of that word, e.g., [(_topid_id, [('word', 0.52), ('ortoken', 0.412)])]
    @abstractmethod
    def get_topics(self):
        pass

