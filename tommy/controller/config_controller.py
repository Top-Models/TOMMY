from typing import Dict, Optional

from tommy.controller.publisher.publisher import Publisher
from tommy.model.config_model import ConfigModel
from tommy.model.project_settings_model import ProjectSettingsModel


class ConfigController(Publisher):
    """
    Controls the access to and changes to the configuration settings.
    """

    def __init__(self, project_settings_controller) -> None:
        """
        Initialize the publisher
        """
        super().__init__()
        self._project_settings_controller = project_settings_controller

    def add_configuration(self, name: str, config: ConfigModel) -> None:
        """
        Add a new configuration with the given name.
        :param name: Name of the configuration
        :param config: Configuration settings
        """
        self._project_settings_controller.add_configuration(name, config)
        # Notify observers of the change
        self.notify()

    def delete_configuration(self, name: str) -> None:
        """
        Delete the configuration with the given name.
        :param name: Name of the configuration to delete
        """
        if name in self._project_settings_controller.get_configurations():
            self._project_settings_controller.delete_configuration(name)
            self.notify()



    def get_configuration(self, name: str) -> Optional[ConfigModel]:
        """
        Get the configuration settings by name.
        :param name: Name of the configuration
        :return: Configuration settings if found, None otherwise
        """
        return self._project_settings_controller.get_configuration(name)

    def list_configurations(self):
        """List all available configurations."""
        return self._project_settings_controller.get_configurations()

    def set_model_refs(self, config_model: ConfigModel):
        """
        Sets the reference to the pconfig_model

        :param config_model: The config_model
        :return: None
        """
        self._config_model = config_model

"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University 
(Department of Information and Computing Sciences)
"""