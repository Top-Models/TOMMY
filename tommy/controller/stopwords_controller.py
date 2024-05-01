from tommy.model.stopwords_model import StopwordsModel
from tommy.support.event_handler import EventHandler


class StopwordsController:
    """A class that handles all stopword related functionality."""
    _stopwords_model: StopwordsModel = None
    _stopwords_model_changed_event: EventHandler[set[str]] = EventHandler()

    @property
    def stopwords_model_changed_event(self) -> EventHandler[set[str]]:
        return self._stopwords_model_changed_event

    @property
    def stopwords_model(self) -> StopwordsModel:
        return self._stopwords_model

    def __init__(self) -> None:
        """Initializes the stopwords controller."""
        super().__init__()

    def set_model_refs(self, stopwords_model: StopwordsModel):
        """Sets the reference to the stopwords model."""
        self._stopwords_model = stopwords_model

    def change_config_model_refs(self, stopwords_model: StopwordsModel):
        """Sets the reference to the stopwords model and updates the
        frontend"""
        self._stopwords_model = stopwords_model
        self._stopwords_model_changed_event.publish(
            stopwords_model.extra_words)

    def update_stopwords(self, words: set[str]) -> None:
        """
        Update the stopwords model with a new list of extra stopwords.

        :param words: The new list of stopwords
        :return: None
        """

        self._stopwords_model.replace(words)


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University 
(Department of Information and Computing Sciences)
"""
