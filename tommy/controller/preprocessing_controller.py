from tommy.model.stopwords_model import StopwordsModel


class PreprocessingController:
    _stopwords_model: StopwordsModel = None

    def __init__(self) -> None:
        pass

    def set_model_refs(self, stopwords_model: StopwordsModel):
        self._stopwords_model = stopwords_model


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University 
(Department of Information and Computing Sciences)
"""
