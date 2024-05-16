import json
import os
from typing import Dict

from PySide6.QtWidgets import QMessageBox

from tommy.model.config_model import ConfigModel
from tommy.support.event_handler import EventHandler
from tommy.model.project_settings_model import ProjectSettingsModel


class ProjectSettingsController:
    """
    The project settings controller class is responsible for handling
    interactions with the project settings.
    """
    _project_settings_model: ProjectSettingsModel = None
    _input_folder_path_changed_event: EventHandler[str]

    @property
    def input_folder_path_changed_event(self) -> EventHandler[str]:
        return self._input_folder_path_changed_event

    # def save_settings_to_file(self) -> None:
    #     """
    #     Save the project settings to a new file in the 'settings' folder as 'ProjectSettings.json'.
    #     :return: None
    #     """
    # settings_data = {
    #     "input_folder_path": os.path.relpath(
    #         self._project_settings_model.input_folder_path,
    #         os.path.dirname(__file__)),
    #     "configs": [config.to_dict() for config in
    #                 self._project_settings_model.configs]
    # }
    # settings_folder_path = os.path.join(os.path.dirname(__file__), "..",
    #                                     "settings")
    # os.makedirs(settings_folder_path,
    #             exist_ok=True)  # Create the 'settings' folder if it doesn't exist
    # file_path = os.path.join(settings_folder_path, "ProjectSettings.json")
    # with open(file_path, "w") as file:
    #     json.dump(settings_data, file, indent=4)
    # QMessageBox.information(None, "Success",
    #                         "Settings saved successfully.")

    # def load_settings_from_file(self) -> None:
    #     """
    #     Load the project settings from a file.
    #     :return: None
    #     """
    # settings_folder_path = os.path.join(os.path.dirname(__file__), "..",
    #                                     "settings")
    # file_path = os.path.join(settings_folder_path, "ProjectSettings.json")
    # if os.path.exists(file_path):
    #     with open(file_path, "r") as file:
    #         settings_data = json.load(file)
    #         input_folder_path = settings_data.get("input_folder_path")
    #         if input_folder_path:
    #             self._project_settings_model.input_folder_path = os.path.join(
    #                 os.path.dirname(__file__), "..", "data",
    #                 input_folder_path)
    #         configs_data = settings_data.get("configs")
    #         if configs_data:
    #             self._project_settings_model.configs.clear()
    #             for config_dict in configs_data:
    #                 config = ConfigModel(config_dict["name"])
    #                 config = ConfigModel.from_dict(config_dict)
    #                 self._project_settings_model.configs.append(config)
    #     self.notify()
    #     QMessageBox.information(None, "Success",
    #                             "Settings loaded successfully.")
    # else:
    #     QMessageBox.warning(None, "Error", "Failed to load settings.")

    def __init__(self) -> None:
        """
        Initialize the publisher
        """
        super().__init__()
        self._input_folder_path_changed_event = EventHandler[str]()

    def set_model_refs(self, project_settings_model: ProjectSettingsModel):
        """
        Sets the reference to the project settings model

        :param project_settings_model: The project settings model
        :return: None
        """
        self._project_settings_model = project_settings_model

    def set_input_folder_path(self, path: str) -> None:
        """
        Set the input folder in the project settings model and notify
        observers of the change to the input folder
        :param path: The path to set
        :return: None
        """
        self._project_settings_model.input_folder_path = path
        self._input_folder_path_changed_event.publish(path)

    def get_input_folder_path(self) -> str:
        """
        Get the input folder from the project settings model
        :return: The path to the input folder
        """
        return self._project_settings_model.input_folder_path


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University
(Department of Information and Computing Sciences)
"""
