from __future__ import annotations

from typing import Optional

from tommy.controller.topic_modelling_runners.abstract_topic_runner import \
    TopicRunner
from tommy.model.corpus_model import CorpusModel
from tommy.model.model_parameters_model import ModelParametersModel
from tommy.model.stopwords_model import StopwordsModel
from tommy.model.topic_model import TopicModel


class ConfigModel:
    """A class representing the configuration."""

    def __init__(self, derive_from: ConfigModel = None):
        self.topic_runner: Optional[TopicRunner] = None
        self.topic_model = TopicModel()
        if derive_from is None:
            self.stopwords_model = StopwordsModel()
            self.model_parameters_model = ModelParametersModel()
            self.corpus_model = CorpusModel()
        else:
            self.stopwords_model = StopwordsModel(
                derive_from.stopwords_model)
            self.model_parameters_model = ModelParametersModel(
                derive_from.model_parameters_model)
            self.corpus_model = CorpusModel(
                derive_from.corpus_model
            )


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University 
(Department of Information and Computing Sciences)
"""
