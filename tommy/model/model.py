from __future__ import annotations

from tommy.model.config_model import ConfigModel
from tommy.model.corpus_model import CorpusModel
from tommy.model.language_model import LanguageModel
from tommy.model.project_settings_model import ProjectSettingsModel
from tommy.support.supported_languages import SupportedLanguage


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

    def to_dict(self) -> dict:
        config_data = {}
        for name, config in self.configs.items():
            config_data[name] = config.to_dict()
        return {
            "input_folder_path": self.project_settings_model.input_folder_path,
            "language": SupportedLanguage.to_string(
                self.language_model.selected_language),
            "configs": config_data,
            "selected_config": self.selected_config_name
        }

    @classmethod
    def from_dict(cls, model_dict: dict) -> Model:
        model = cls()
        model.project_settings_model.input_folder_path = model_dict[
            "input_folder_path"]
        model.language_model.selected_language = (
            SupportedLanguage.from_string(model_dict["language"]))
        configs_data = model_dict["configs"]
        model.configs.clear()
        for name, config_dict in configs_data.items():
            config = ConfigModel.from_dict(config_dict)
            model.configs[name] = config
        model.selected_config_name = model_dict["selected_config"]
        return model


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University
(Department of Information and Computing Sciences)
"""
