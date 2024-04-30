from tommy.model.corpus_model import CorpusModel
from tommy.model.model_parameters_model import ModelParametersModel
from tommy.model.stopwords_model import StopwordsModel
from tommy.model.topic_model import TopicModel


class ConfigModel:
    """A class representing the configuration."""

    def __init__(self):
        self.stopwords_model = StopwordsModel()
        self.model_parameters_model = ModelParametersModel()
        self.corpus_model = CorpusModel()
        self.topic_model = TopicModel()


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University 
(Department of Information and Computing Sciences)
"""
