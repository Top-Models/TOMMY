from tommy.model.synonyms_model import SynonymsModel


class SynonymsController:
    """A class that handles all stopword related functionality."""
    _synonyms_model: SynonymsModel = None

    @property
    def stopwords_model(self) -> SynonymsModel:
        return self._synonyms_model

    def __init__(self) -> None:
        """Initializes the stopwords controller."""
        super().__init__()

    def set_model_refs(self, stopwords_model: SynonymsModel):
        """Sets the reference to the stopwords model."""
        self._synonyms_model = stopwords_model

    def update_synonyms(self, synonyms_mapping: dict[str, list[str]]) -> None:
        """
        Update the synonyms model with a new dict of  synonyms.

        :param synonyms_mapping: The new duct of synonyms
        :return: None
        """

        self._synonyms_model.replace(synonyms_mapping)


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University 
(Department of Information and Computing Sciences)
"""
