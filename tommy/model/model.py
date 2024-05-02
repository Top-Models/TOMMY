from tommy.model.config_model import ConfigModel
from tommy.model.project_settings_model import ProjectSettingsModel


class Model:
    default_config_name = "Config 1"

    configs: dict[str, ConfigModel] = {}
    selected_config_name: str
    project_settings_model: ProjectSettingsModel

    def __init__(self):
        first_config = ConfigModel()

        self.project_settings_model = ProjectSettingsModel()
        self.selected_config_name = Model.default_config_name
        self.configs[Model.default_config_name] = first_config

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
        # TODO: copy current configuration into new configmodel
        return ConfigModel(self.config_model)


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University 
(Department of Information and Computing Sciences)
"""
