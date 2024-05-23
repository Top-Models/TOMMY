import json
import os

from PySide6.QtWidgets import QMessageBox

from tommy.model.model import Model
from tommy.support.event_handler import EventHandler


class SavingLoadingController:

    def __init__(self):
        # if a file is loaded or saved, the filepath is set so that the user
        # doesn't have to specify the file path again when saving
        self.filepath = None

        self._model: Model = None

        # event that is triggered when the model is changed
        self._model_changed_event: EventHandler[Model] = EventHandler()

    @property
    def model_changed_event(self) -> EventHandler[Model]:
        return self._model_changed_event

    # TODO: call set model refs and set controller refs and add them to the
    #  controller and model references test
    def set_model_refs(self, model: Model) -> None:
        """
        Set the reference to the model.
        :param model: The model
        :return: None
        """
        self._model = model

    def save_settings_to_file(self, filepath: str) -> None:
        """
        Save the project settings to a new file specified by the filepath.
        :param filepath: The filepath where the settings should be saved
        :return: None
        """
        self.filepath = filepath
        settings_data = self._model.to_dict()
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, "w") as file:
            json.dump(settings_data, file, indent=4)
        QMessageBox.information(None, "Success",
                                "Settings saved successfully.")

    def load_settings_from_file(self, filepath) -> None:
        """
        Load the project settings from a file.
        :return: None
        """
        self.filepath = filepath
        if os.path.exists(filepath):
            with open(filepath, "r") as file:
                settings_data = json.load(file)
                new_model = Model.from_dict(settings_data)
                self._model_changed_event.publish(new_model)
            QMessageBox.information(None, "Success",
                                    "Settings loaded successfully.")
        else:
            QMessageBox.warning(None, "Error", "Failed to load settings.")
