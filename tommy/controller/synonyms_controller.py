from tommy.model.synonyms_model import SynonymsModel


class SynonymsController:
    """A class that handles all synonym related functionality."""
    _synonyms_model: SynonymsModel = None

    @property
    def stopwords_model(self) -> SynonymsModel:
        return self._synonyms_model

    def __init__(self) -> None:
        """Initializes the synonyms controller."""
        super().__init__()

    def set_model_refs(self, synonyms_model: SynonymsModel):
        """Sets the reference to the synonyms model."""
        self._synonyms_model = synonyms_model

    def update_synonyms(self, synonyms: dict[str, str]) -> None:
        """
        Update the synonyms model with a new dictionary of synonyms.

        :param synonyms: A dictionary where the keys represent source words
        and the values represent target words.
        :return: None
        """

        self._synonyms_model.replace(synonyms)


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University 
(Department of Information and Computing Sciences)
"""
