from tommy.model.model_parameters_model import ModelParametersModel
from tommy.model.topic_model import TopicModel


class TopicModellingController:
    model_parameters_model: ModelParametersModel = None
    topic_model: TopicModel = None

    @staticmethod
    def set_model_parameters_model(parameters_model: ModelParametersModel) -> None:
        TopicModellingController.model_parameters_model = parameters_model

    @staticmethod
    def set_topic_model(topic_model: TopicModel) -> None:
        TopicModellingController.topic_model = topic_model


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University 
(Department of Information and Computing Sciences)
"""
