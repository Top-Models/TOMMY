import json
import os
from typing import Dict

from tommy.controller.publisher.publisher import Publisher
from tommy.model.config_model import ConfigModel
from tommy.model.project_settings_model import ProjectSettingsModel


class ProjectSettingsController(Publisher):
    """
    The project settings controller class is responsible for handling interactions with
    the project settings.
    """
    _project_settings_model: ProjectSettingsModel = None

    def set_input_folder_path(self, path: str) -> None:
        """
        Set the input folder in the project settings model and notify
        observers of the change to the input folder
        :param path: The path to set
        :return: None
        """
        self._project_settings_model.input_folder_path = path
        self.notify()

    def get_input_folder_path(self) -> str:
        """
        Get the input folder from the project settings model
        :return: The path to the input folder
        """
        return self._project_settings_model.input_folder_path

    def add_configuration(self, name: str, config: ConfigModel) -> None:
        """
        Add a new configuration to the project settings model.
        :param name: Name of the configuration
        :param config: Configuration settings
        """
        # Add the configuration to the project settings model
        self._project_settings_model.configs.append(config)
        # Notify observers of the change
        self.notify()

    def delete_configuration(self, name: str, config: ConfigModel) -> None:
        """
        delete a configuration to the project settings model.
        :param name: Name of the configuration
        :param config: Configuration settings
        """
        # Add the configuration to the project settings model
        self._project_settings_model.configs.remove(config)
        # Notify observers of the change
        self.notify()

    def get_configurations(self) -> Dict[str, ConfigModel]:
        """
        Get all configurations from the project settings model.
        :return: A dictionary of configurations
        """
        return {config.name: config for config in
                self._project_settings_model.configs}

    def get_configuration(self, name: str) -> ConfigModel:
        """
        Get a configuration by name from the project settings model.
        :param name: Name of the configuration to retrieve
        :return: The configuration model
        """
        for config in self._project_settings_model.configs:
            if config.name == name:
                return config
        return None

    def save_settings_to_file(self, file_name: str) -> None:
        """
        Save the project settings to a new file in the data folder.
        :param file_name: Name of the file to save the settings
        :return: None
        """
        settings_data = {
            "input_folder_path": os.path.relpath(
                self._project_settings_model.input_folder_path,
                os.path.dirname(__file__)),
            "configs": [config.to_dict() for config in
                        self._project_settings_model.configs]
        }
        file_path = os.path.join(os.path.dirname(__file__), "..", "data",
                                 file_name)
        with open(file_path, "w") as file:
            json.dump(settings_data, file, indent=4)

    def load_settings_from_file(self, file_name: str) -> None:
        """
        Load the project settings from a file.
        :param file_name: Name of the file containing the settings
        :return: None
        """
        file_path = os.path.join(os.path.dirname(__file__), "..", "data",
                                 file_name)
        if os.path.exists(file_path):
            with open(file_path, "r") as file:
                settings_data = json.load(file)
                input_folder_path = settings_data.get("input_folder_path")
                if input_folder_path:
                    self._project_settings_model.input_folder_path = os.path.join(
                        os.path.dirname(__file__), "..", "data",
                        input_folder_path)
                configs_data = settings_data.get("configs")
                if configs_data:
                    self._project_settings_model.configs.clear()
                    for config_dict in configs_data:
                        config = ConfigModel(config_dict["name"])
                        config = ConfigModel.from_dict(config_dict)
                        self._project_settings_model.configs.append(config)
            self.notify()

    def __init__(self) -> None:
        """
        Initialize the publisher
        """
        super().__init__()

    def set_model_refs(self, project_settings_model: ProjectSettingsModel):
        """
        Sets the reference to the project settings model

        :param project_settings_model: The project settings model
        :return: None
        """
        self._project_settings_model = project_settings_model


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University 
(Department of Information and Computing Sciences)
"""
