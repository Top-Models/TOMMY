from tommy.model.stopwords_model import StopWordsModel


class StopwordsController:
    """A class that handles all stop word related functionality."""
    stopwords_model: StopWordsModel = None

    @staticmethod
    def set_stopwords_model(stopwords_model: StopWordsModel):
        StopwordsController.stopwords_model = stopwords_model

    @staticmethod
    def add_stopword(word: str) -> None:
        """
        Add a stopword to the stopwords model.

        :param word: The stopword to add
        :return: None
        """
        StopwordsController.stopwords_model.add(word)

    @staticmethod
    def remove_stopword(word: str) -> None:
        """
        Remove a stopword from the stopwords model.

        :param word: The stopword to remove
        :return: None
        """
        StopwordsController.stopwords_model.remove(word)


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University 
(Department of Information and Computing Sciences)
"""
