from collections.abc import Iterable

from interactive_topic_modeling.model.stopwords_model import StopWordsModel


class StopWordsController:
    def __init__(self, stopwords_model: StopWordsModel):
        self.stopwords_model = stopwords_model

    def add_stopwords(self, *args: str | Iterable[str]) -> None:
        """
        Add one or more stop words
        :param args: The word(s) to add to the iterable.
        :return: None.
        """
        # Only 1 argument and it's a list or tuple
        if len(args) == 1 and isinstance(args[0], Iterable):
            words = args[0]
        # Otherwise the arguments should be the words themselves
        else:
            words = args
        # Add the words to the set
        self.stopwords_model.add_stopwords(words)
