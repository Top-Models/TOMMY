from typing import Dict, Optional

from tommy.model.config_model import ConfigModel
from tommy.model.model import Model
from tommy.model.project_settings_model import ProjectSettingsModel
from tommy.support.event_handler import EventHandler


class ConfigController:
    """
    Controls the access to and changes to the configuration settings.
    """
    _config_switched_event: EventHandler[ConfigModel] = EventHandler()
    _config_list_changed_event: EventHandler[list[str]] = EventHandler()
    _model: Model = None

    # TODO: add docstring to many methods

    def set_model_refs(self, model: Model) -> None:
        """
        Set a reference to the model so this class can manage the
        configurations
        :param model: The model
        :return: None
        """
        self._model = model

    def switch_configuration(self, name: str) -> bool:
        config_exists = name in self.get_configuration_names()
        if config_exists:
            self._model.selected_config_name = name
            self._config_switched_event.publish(self._model.config_model)
        return config_exists

    def get_configuration_names(self) -> list[str]:
        return list(self._model.configs.keys())

    def add_configuration(self, name: str) -> bool:
        """
        Add a new configuration with the given name and switch to the new
        configuration
        :param name: Name of the configuration
        :param config: Configuration settings
        :return: Whether the config could successfully be created. Creating a
        config fails if a config with that name already exists
        """
        if name in self.get_configuration_names():
            return False

        config = self._model.create_configuration()
        self._model.configs[name] = config
        self._config_list_changed_event.publish(
            self.get_configuration_names())
        self.switch_configuration(name)
        return True

    def delete_configuration(self, name: str) -> bool:
        """
        Delete the configuration with the given name. If it is the currently
        selected configuration, switch to the previous configuration. If the
        currently selected configuration is the first one, switch to the
        next one instead
        :param name: Name of the configuration to delete
        :return: Whether or not deletion succeeded. Deletion of a
        configuration fails if the configuration name does not exist or if
        it is the only configuration
        """
        configs = self.get_configuration_names()
        if len(configs) < 2:
            return False

        if name not in configs:
            return False

        if name == self._model.selected_config_name:
            # Switch to the previous config. If the current config is
            # already the first config, switch to the next config instead.
            index = configs.index(name)
            new_index = index - 1 if index > 0 else 1
            self.switch_configuration(configs[new_index])

        self._model.configs.pop(name)
        self._config_list_changed_event.publish(self.get_configuration_names())
        return True

    def get_selected_configuration(self) -> str:
        """
        Get the name of the currently selected configuration.
        :return: The name of the configuration
        """
        return self._model.selected_config_name


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University 
(Department of Information and Computing Sciences)
"""
