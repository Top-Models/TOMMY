from __future__ import annotations

from dataclasses import dataclass
from tommy.support.model_type import ModelType


@dataclass
class ModelParametersModel:
    """A class representing the topic modelling parameters."""
    default_n_topics: int = 3
    default_model_type: ModelType = ModelType.LDA
    default_word_amount: int = 10
    default_alpha: float = 1.0
    default_beta: float = 0.01
    default_alpha_beta_custom_enabled: bool = False

    def __init__(self, derive_from: ModelParametersModel = None):
        """
        Create an instance of ModelParametersModel
        :param derive_from: If derive_from is None, then all parameters are
        set to the default value. If derive_from is set to an instance of
        ModelParametersModel, all parameters will be copied from there
        """
        if derive_from is None:
            self.n_topics: int = ModelParametersModel.default_n_topics
            self.model_type: ModelType = (
                ModelParametersModel.default_model_type)
            self.word_amount: int = ModelParametersModel.default_word_amount
            self.alpha: float = ModelParametersModel.default_alpha
            self.beta: float = ModelParametersModel.default_beta
            self.alpha_beta_custom_enabled: bool = (
                ModelParametersModel.default_alpha_beta_custom_enabled)
        else:
            self.n_topics = derive_from.n_topics
            self.model_type = derive_from.model_type
            self.word_amount = derive_from.word_amount
            self.alpha = derive_from.alpha
            self.beta = derive_from.beta
            self.alpha_beta_custom_enabled = (
                derive_from.alpha_beta_custom_enabled)

    def to_dict(self):
        """
        Convert the model parameters object to a dictionary.
        :return: Dictionary representation of the model parameters
        """
        return {
            "n_topics": self.n_topics,
            "model_type": self.model_type.value
        }

    @classmethod
    def from_dict(cls, model_parameters_dict):
        """
        Create a ModelParametersModel instance from a dictionary representation.
        :param model_parameters_dict: Dictionary representation of the model parameters
        :return: ModelParametersModel instance
        """
        n_topics = model_parameters_dict.get("n_topics", 3)
        model_type_value = model_parameters_dict.get("model_type",
                                                     ModelType.LDA.value)
        model_type = ModelType(model_type_value)
        return cls(n_topics=n_topics, model_type=model_type)


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University
(Department of Information and Computing Sciences)
"""
