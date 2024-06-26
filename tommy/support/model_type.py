from __future__ import annotations

from enum import Enum


class ModelType(Enum):
    """An enumeration of the types of models."""
    LDA = 1
    NMF = 2
    BERTopic = 3

    @staticmethod
    def from_string(model_type: str) -> ModelType:
        """
        Convert a string to a ModelType.
        :param model_type: The string to convert
        :return: The ModelType
        """
        match model_type:
            case "LDA":
                return ModelType.LDA
            case "BERTopic":
                return ModelType.BERTopic
            case "NMF":
                return ModelType.NMF
            case _:
                raise ValueError(f"Model type {model_type} not recognized")

    @staticmethod
    def to_string(model_type: ModelType) -> str:
        """
        Convert a ModelType to a string.
        :param model_type: The ModelType to convert
        :return: The string
        """
        match model_type:
            case ModelType.LDA:
                return "LDA"
            case ModelType.BERTopic:
                return "BERTopic"
            case ModelType.NMF:
                return "NMF"
            case _:
                raise ValueError(f"Model type {model_type} not recognized")


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University
(Department of Information and Computing Sciences)
"""
