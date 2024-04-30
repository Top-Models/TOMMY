from tommy.model.model_parameters_model import ModelParametersModel
from tommy.support.model_type import ModelType


class ModelParametersController:
    """
    Controls the access to and changes to the parameters to be used in topic
    modelling
    """
    _parameters_model: ModelParametersModel = None

    def set_model_refs(self,
                       parameters_model: ModelParametersModel) -> None:
        """Set the reference to the model-parameters-model"""
        self._parameters_model = parameters_model

    def set_model_word_amount(self, word_amount: int) -> None:
        """Set the amount of words to be displayed per topic"""
        self._parameters_model.word_amount = word_amount

    def get_model_word_amount(self) -> int:
        """Return the amount of words to be displayed per topic"""
        return self._parameters_model.word_amount

    def set_model_alpha_beta_custom_enabled(self, enabled: bool) -> None:
        """
        Set whether the alpha and beta parameters should be set manually
        :param enabled: whether the parameters should be set manually
        """
        self._parameters_model.alpha_beta_custom_enabled = enabled

    def get_model_alpha_beta_custom_enabled(self) -> bool:
        """
        Return whether the alpha and beta parameters
        should be set manually
        """
        return self._parameters_model.alpha_beta_custom_enabled

    def set_model_alpha(self, alpha: float) -> None:
        """Set the alpha parameter for the topic modelling"""
        self._parameters_model.alpha = alpha

    def get_model_alpha(self) -> float:
        """Return the alpha parameter for the topic modelling"""
        return self._parameters_model.alpha

    def set_model_beta(self, beta: float) -> None:
        """Set the beta parameter for the topic modelling"""
        self._parameters_model.beta = beta

    def get_model_beta(self) -> float:
        """Return the beta parameter for the topic modelling"""
        return self._parameters_model.beta

    def set_model_n_topics(self, n_topics: int) -> None:
        """
        Set the number of topics to use in the topic modelling
        :param n_topics: the desired number of topics
        """
        self._parameters_model.n_topics = n_topics

    def get_model_n_topics(self) -> int:
        """Return the number of topics the topic modelling will find"""
        return self._parameters_model.n_topics

    def set_model_type(self, model_type: ModelType) -> None:
        """
        Set the type of topic modelling algorithm to be run
        :param model_type: the algorithm type to be run
        """
        self._parameters_model.model_type = model_type

    def get_model_type(self) -> ModelType:
        """Return the type of topic modelling algorithm to be run"""
        return self._parameters_model.model_type


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University 
(Department of Information and Computing Sciences)
"""
