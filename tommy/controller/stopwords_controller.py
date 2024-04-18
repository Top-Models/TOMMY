from tommy.support.event_handler import EventHandler
from tommy.model.stopwords_model import StopwordsModel


class StopwordsController:
    """A class that handles all stopword related functionality."""
    _stopwords_model: StopwordsModel = None
    _stopwords_changed_event: EventHandler[StopwordsModel]

    @property
    def stopwords_model(self) -> StopwordsModel:
        return self._stopwords_model

    @property
    def stopwords_changed_event(self) -> EventHandler[StopwordsModel]:
        return self._stopwords_changed_event

    def __init__(self) -> None:
        """Initializes the stopwords controller."""
        super().__init__()
        self._stopwords_changed_event = EventHandler[StopwordsModel]()

    def set_model_refs(self, stopwords_model: StopwordsModel):
        """Sets the reference to the stopwords model."""
        self._stopwords_model = stopwords_model

    def update_stopwords(self, words: list[str]) -> None:
        """
        Update the stopwords model with a new list of extra stopwords.

        :param words: The new list of stopwords
        :return: None
        """

        self._stopwords_model.replace(words)
        self._stopwords_changed_event.publish(self._stopwords_model)

    # TODO: this method will be deprecated in the new UI redesign
    def add_stopword(self, word: str) -> None:
        """
        Add a new stopword to the stopwords model.

        :param word: The new stopword
        :return: None
        """
        self._stopwords_model.add(word)
        self._stopwords_changed_event.publish(self._stopwords_model)

    # TODO: this method will be deprecated in the new UI redesign
    def remove_stopword(self, word: str) -> None:
        """
        Remove a stopword from the stopwords model.

        :param word: The stopword to be removed
        :return: None
        """
        self._stopwords_model.remove(word)
        self._stopwords_changed_event.publish(self._stopwords_model)


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University 
(Department of Information and Computing Sciences)
"""
