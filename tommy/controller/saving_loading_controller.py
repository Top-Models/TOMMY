import json
import os

from PySide6.QtWidgets import QMessageBox

from tommy.controller.config_controller import ConfigController
from tommy.model.model import Model


class SavingLoadingController:

    def __init__(self):
        self._model: Model = None
        self._config_controller: ConfigController = None

    # TODO: call set model refs and set controller refs and add them to the
    #  controller and model references test
    def set_model_refs(self, model: Model) -> None:
        """
        Set the reference to the model
        :param model: The model
        :return: None
        """
        self._model = model

    def set_controller_refs(self, config_controller: ConfigController) -> None:
        """
        Set the reference to the config controller
        :param config_controller: The config controller
        :return: None
        """
        self._config_controller = config_controller

    def save_settings_to_file(self) -> None:
        """
        Save the project settings to a new file in the 'settings' folder as 'ProjectSettings.json'.
        :return: None
        """
        settings_data = self._model.to_dict()

        settings_folder_path = os.path.join(os.path.dirname(__file__), "..",
                                            "settings")
        os.makedirs(settings_folder_path,
                    exist_ok=True)  # Create the 'settings' folder if it doesn't exist
        file_path = os.path.join(settings_folder_path, "ProjectSettings.json")
        with open(file_path, "w") as file:
            json.dump(settings_data, file, indent=4)
        QMessageBox.information(None, "Success",
                                "Settings saved successfully.")

    def load_settings_from_file(self) -> None:
        """
        Load the project settings from a file.
        :return: None
        """
        settings_folder_path = os.path.join(os.path.dirname(__file__), "..",
                                            "settings")
        file_path = os.path.join(settings_folder_path, "ProjectSettings.json")
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
            QMessageBox.information(None, "Success",
                                    "Settings loaded successfully.")
        else:
            QMessageBox.warning(None, "Error", "Failed to load settings.")
