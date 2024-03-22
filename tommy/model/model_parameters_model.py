from dataclasses import dataclass
from tommy.support.model_type import ModelType


@dataclass
class ModelParametersModel:
    """A class representing the topic modelling parameters."""
    n_topics: int = 3
    model_type: ModelType = ModelType.LDA


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University 
(Department of Information and Computing Sciences)
"""
