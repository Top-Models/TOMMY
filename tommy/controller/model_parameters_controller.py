from tommy.model.model_parameters_model import ModelParametersModel
from tommy.support.model_type import ModelType


class ModelParametersController:
    _parameters_model: ModelParametersModel = None

    def set_model_refs(self,
                       parameters_model: ModelParametersModel) -> None:
        self._parameters_model = parameters_model

    def set_model_n_topics(self, n_topics: int) -> None:
        self._parameters_model.n_topics = n_topics

    def get_model_n_topics(self) -> int:
        return self._parameters_model.n_topics

    def set_model_type(self, model_type: ModelType) -> None:
        self._parameters_model.model_type = model_type

    def get_model_type(self) -> ModelType:
        return self._parameters_model.model_type


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University 
(Department of Information and Computing Sciences)
"""
