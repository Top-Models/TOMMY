from tommy.controller.publisher.publisher import Publisher
from tommy.model.stopwords_model import StopWordsModel


class StopwordsController(Publisher):
    """A class that handles all stopword related functionality."""
    stopwords_model: StopWordsModel = None

    @staticmethod
    def set_stopwords_model(stopwords_model: StopWordsModel):
        StopwordsController.stopwords_model = stopwords_model

    @staticmethod
    def update_stopwords(words: list[str]) -> None:
        """
        Update the stopwords model with a new list of extra stopwords.

        :param words: The new list of stopwords
        :return: None
        """

        StopwordsController.stopwords_model.replace(words)


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University 
(Department of Information and Computing Sciences)
"""
