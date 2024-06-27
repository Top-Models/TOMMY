from __future__ import annotations

from dataclasses import dataclass

from tommy.support.model_type import ModelType
from tommy.support.parameter_limits import *


@dataclass
class ModelParametersModel:
    """A class representing the topic modelling parameters."""
    default_n_topics: int = 3
    default_model_type: ModelType = ModelType.LDA
    default_word_amount: int = 10
    default_alpha: float = 0.33
    default_beta: float = 0.33
    default_alpha_beta_custom_enabled: bool = False
    default_bert_min_df: float | None = None
    default_bert_max_features: int | None = None

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
            self.bert_max_features = (ModelParametersModel.
                                      default_bert_max_features)
        else:
            self.n_topics = derive_from.n_topics
            self.model_type = derive_from.model_type
            self.word_amount = derive_from.word_amount
            self.alpha = derive_from.alpha
            self.beta = derive_from.beta
            self.alpha_beta_custom_enabled = (
                derive_from.alpha_beta_custom_enabled)
            self.bert_min_df = derive_from.bert_min_df
            self.bert_max_features = derive_from.bert_max_features

    def to_dict(self):
        """
        Convert the model parameters object to a dictionary.
        :return: Dictionary representation of the model parameters
        """
        return {
            "n_topics": self.n_topics,
            "model_type": ModelType.to_string(self.model_type),
            "word_amount": self.word_amount,
            "alpha": self.alpha,
            "beta": self.beta,
            "alpha_beta_custom_enabled": self.alpha_beta_custom_enabled,
            "bert_min_df": "None" if self.bert_min_df is None else
            self.bert_min_df,
            "bert_max_features": "None" if self.bert_max_features is None
            else self.bert_max_features
        }

    @classmethod
    def from_dict(cls, model_parameters_dict: dict) -> ModelParametersModel:
        """
        Create a ModelParametersModel instance from a dictionary
        representation.
        :param model_parameters_dict: Dictionary representation of the model
        parameters
        :return: ModelParametersModel instance
        """
        model_params_model = cls()
        # get the values from the dictionary
        num_topics = model_parameters_dict["n_topics"]
        model_type = model_parameters_dict["model_type"]
        word_amount = model_parameters_dict["word_amount"]
        alpha = model_parameters_dict["alpha"]
        beta = model_parameters_dict["beta"]
        alpha_beta_custom_enabled = model_parameters_dict[
            "alpha_beta_custom_enabled"]
        bert_min_df = model_parameters_dict["bert_min_df"]
        bert_max_features = model_parameters_dict["bert_max_features"]

        # check if the values are of the correct type and within the correct
        # range
        if (not isinstance(num_topics, int) or
                num_topics < num_topics_min_value or
                num_topics > num_topics_max_value):
            raise ValueError(f"Number of topics should be an integer between"
                             f" {num_topics_min_value} and "
                             f"{num_topics_max_value}, but is:"
                             f" {model_params_model.n_topics}")

        if not isinstance(model_type, str):
            raise ValueError("Model type should be a string, but is not")

        if (not isinstance(word_amount, int) or
                word_amount < amount_of_words_min_value or
                word_amount > amount_of_words_max_value):
            raise ValueError(f"Amount of words should be an integer between"
                             f" {amount_of_words_min_value} and "
                             f"{amount_of_words_max_value}, but is:"
                             f" {model_params_model.word_amount}")

        if not isinstance(alpha, float) or alpha <= alpha_min_value:
            raise ValueError(f"Alpha should be a float greater than"
                             f" to {alpha_min_value}, but is:"
                             f" {model_params_model.alpha}")

        if not isinstance(beta, float) or beta <= beta_min_value:
            raise ValueError(f"Beta should be a float greater than"
                             f" to {beta_min_value}, but is:"
                             f" {model_params_model.beta}")

        if not isinstance(alpha_beta_custom_enabled, bool):
            raise ValueError("Alpha beta custom enabled should be a boolean,"
                             " but is not")

        if bert_min_df != "None" and (not isinstance(bert_min_df, float) or
                                      bert_min_df < min_df_min_value or
                                      bert_min_df > min_df_max_value):
            raise ValueError(f"Bert min df should be a float between"
                             f" {min_df_min_value} and {min_df_max_value},"
                             f" but is: {model_params_model.bert_min_df}")

        if bert_max_features != "None" and (
                not isinstance(bert_max_features, int) or
                bert_max_features < max_features_min_value or
                bert_max_features > max_features_max_value):
            raise ValueError(f"Bert max features should be an integer between"
                             f" {max_features_min_value} and"
                             f" {max_features_max_value}, but is:"
                             f" {model_params_model.bert_max_features}")

        # set the values in the model
        model_params_model.n_topics = num_topics
        model_params_model.model_type = ModelType.from_string(model_type)
        model_params_model.word_amount = word_amount
        model_params_model.alpha = alpha
        model_params_model.beta = beta
        model_params_model.alpha_beta_custom_enabled = (
            alpha_beta_custom_enabled)
        model_params_model.bert_min_df = (None if bert_min_df == "None"
                                          else bert_min_df)
        model_params_model.bert_max_features = (
            None if bert_max_features == "None"
            else bert_max_features)

        return model_params_model


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University
(Department of Information and Computing Sciences)
"""
