from dataclasses import dataclass
from tommy.support.model_type import ModelType


@dataclass
class ModelParametersModel:
    """A class representing the topic modelling parameters."""
    n_topics: int = 3
    model_type: ModelType = ModelType.LDA

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
