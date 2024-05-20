from tommy.model.config_model import ConfigModel
from tommy.model.corpus_model import CorpusModel
from tommy.model.language_model import LanguageModel
from tommy.model.project_settings_model import ProjectSettingsModel
from tommy.model.stopwords_model import StopwordsModel
from tommy.model.model_parameters_model import ModelParametersModel
from tommy.model.synonyms_model import SynonymsModel
from tommy.model.topic_model import TopicModel


class Model:
    default_config_name = "Config 1"

    def __init__(self):
        self.language_model: LanguageModel = LanguageModel()
        self.project_settings_model: ProjectSettingsModel = (
            ProjectSettingsModel())

        first_config = ConfigModel()
        self.selected_config_name: str = Model.default_config_name

        # add fist configuration to dictionary using the default config name
        self.configs: dict[str, ConfigModel] = {
            Model.default_config_name: first_config}

    @property
    def config_model(self):
        return self.configs[self.selected_config_name]

    @property
    def stopwords_model(self):
        return self.config_model.stopwords_model

    @property
    def model_parameters_model(self):
        return self.config_model.model_parameters_model

    @property
    def corpus_model(self):
        return self.config_model.corpus_model

    @property
    def topic_model(self):
        return self.config_model.topic_model

    def create_configuration(self) -> ConfigModel:
        """
        Create a new configuration based on the current configuration
        :return: The newly created config model
        """
        return ConfigModel(self.config_model)


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University
(Department of Information and Computing Sciences)
"""
