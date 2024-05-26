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
    default_bert_min_df: int | None = None

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
            self.bert_min_df = ModelParametersModel.default_bert_min_df
        else:
            self.n_topics = derive_from.n_topics
            self.model_type = derive_from.model_type
            self.word_amount = derive_from.word_amount
            self.alpha = derive_from.alpha
            self.beta = derive_from.beta
            self.alpha_beta_custom_enabled = (
                derive_from.alpha_beta_custom_enabled)
            self.bert_min_df = derive_from.bert_min_df


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University
(Department of Information and Computing Sciences)
"""
