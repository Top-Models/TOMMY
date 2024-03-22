from tommy.model.model_parameters_model import ModelParametersModel
from tommy.support.model_type import ModelType


class ModelParametersController:
    parameters_model: ModelParametersModel = None

    @staticmethod
    def set_model_parameters_model(parameters_model: ModelParametersModel) -> (
            None):
        ModelParametersController.parameters_model = parameters_model

    @staticmethod
    def set_model_n_topics(n_topics: int) -> None:
        ModelParametersController.parameters_model.n_topics = n_topics

    @staticmethod
    def get_model_n_topics() -> int:
        return ModelParametersController.parameters_model.n_topics

    @staticmethod
    def set_model_type(model_type) -> None:
        ModelParametersController.parameters_model.model_type = model_type

    @staticmethod
    def get_model_type() -> ModelType:
        return ModelParametersController.parameters_model.model_type


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University 
(Department of Information and Computing Sciences)
"""
