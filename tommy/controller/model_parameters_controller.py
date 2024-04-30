from tommy.model.model_parameters_model import ModelParametersModel
from tommy.support.event_handler import EventHandler
from tommy.support.model_type import ModelType


class ModelParametersController:
    """
    Controls the access to and changes to the parameters to be used in topic
    modelling
    """
    _parameters_model: ModelParametersModel = None
    _params_changed_event: EventHandler[tuple[int, ModelType]] = EventHandler()

    def set_model_refs(self,
                       parameters_model: ModelParametersModel) -> None:
        """Set the reference to the model-parameters-model"""
        self._parameters_model = parameters_model

    def set_model_n_topics(self, n_topics: int) -> None:
        """
        Set the number of topics to use in the topic modelling
        :param n_topics: the desired number of topics
        """
        self._parameters_model.n_topics = n_topics
        self._params_changed_event.publish((n_topics, self.get_model_type()))

    def get_model_n_topics(self) -> int:
        """Return the number of topics the topic modelling will find"""
        return self._parameters_model.n_topics

    def set_model_type(self, model_type: ModelType) -> None:
        """
        Set the type of topic modelling algorithm to be run
        :param model_type: the algorithm type to be run
        """
        self._parameters_model.model_type = model_type
        self._params_changed_event.publish((self.get_model_n_topics(),
                                            model_type))

    def get_model_type(self) -> ModelType:
        """Return the type of topic modelling algorithm to be run"""
        return self._parameters_model.model_type


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University 
(Department of Information and Computing Sciences)
"""
