from tommy.model.corpus_model import CorpusModel
from tommy.model.language_model import LanguageModel
from tommy.model.project_settings_model import ProjectSettingsModel
from tommy.model.stopwords_model import StopwordsModel
from tommy.model.model_parameters_model import ModelParametersModel
from tommy.model.topic_model import TopicModel


class Model:
    stopwords_model: StopwordsModel
    model_parameters_model: ModelParametersModel
    project_settings_model: ProjectSettingsModel
    corpus_model: CorpusModel
    topic_model: TopicModel
    language_model: LanguageModel

    def __init__(self):
        self.stopwords_model = StopwordsModel()
        self.model_parameters_model = ModelParametersModel()
        self.project_settings_model = ProjectSettingsModel()
        self.corpus_model = CorpusModel()
        self.topic_model = TopicModel()
        self.language_model = LanguageModel()


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University
(Department of Information and Computing Sciences)
"""
