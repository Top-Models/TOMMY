from tommy.model.model_parameters_model import ModelParametersModel
from tommy.model.topic_model import TopicModel


class TopicModellingController:
    model_parameters_model: ModelParametersModel = None
    topic_model: TopicModel = None

    def __init__(self) -> None:
        pass

    def set_model_refs(self, parameters_model: ModelParametersModel,
                       topic_model: TopicModel) -> None:
        self.model_parameters_model = parameters_model
        self.topic_model = topic_model


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University 
(Department of Information and Computing Sciences)
"""
