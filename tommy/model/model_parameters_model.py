from __future__ import annotations

from dataclasses import dataclass
from tommy.support.model_type import ModelType


@dataclass
class ModelParametersModel:
    """A class representing the topic modelling parameters."""

    default_n_topics: int = 3
    default_model_type: ModelType = ModelType.LDA

    def __init__(self, derive_from: ModelParametersModel = None):
        if derive_from is None:
            self.n_topics: int = ModelParametersModel.default_n_topics
            self.model_type: ModelType = (
                ModelParametersModel.default_model_type)
        else:
            self.n_topics = derive_from.n_topics
            self.model_type = derive_from.model_type


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University 
(Department of Information and Computing Sciences)
"""
