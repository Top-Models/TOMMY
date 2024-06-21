import json
import os

from tommy.model.model import Model
from tommy.support.event_handler import EventHandler


def dict_raise_on_duplicates(ordered_pairs):
    """Reject duplicate keys."""
    d = {}
    for k, v in ordered_pairs:
        if k in d:
            raise ValueError(f"duplicate key: {k}")
        else:
            d[k] = v
    return d


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

    def set_model_refs(self, model: Model) -> None:
        """
        Set the reference to the model.
        :param model: The model
        :return: None
        """
        self._model = model

    def save_settings_to_file(self, filepath: str) -> list[str]:
        """
        Save the project settings to a new file specified by the filepath.
        :param filepath: The filepath where the settings should be saved
        :return: None
        """
        self.filepath = filepath
        settings_data = self._model.to_dict()
        try:
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            with open(filepath, "w") as file:
                json.dump(settings_data, file, indent=4)
            return []
        except OSError as e:
            return [f"Er is een fout opgetreden bij het opslaan van het "
                    f"bestand:\n{filepath}.\nProbleem:\n{repr(e)}"]

    def load_settings_from_file(self, filepath) -> list[str]:
        """
        Load the project settings from a file.
        :return: None
        """
        self.filepath = filepath
        if not os.path.exists(filepath):
            return [f"Dit pad bestaat niet:\n{filepath}"]
        try:
            with (open(filepath, "r") as file):
                settings_data = (
                    json.load(file,
                              object_pairs_hook=dict_raise_on_duplicates))
                new_model = Model.from_dict(settings_data)
                self._model_changed_event.publish(new_model)
            return []
        except json.JSONDecodeError as e:
            return [f"Dit bestand is geen geldig JSON bestand:\n"
                    f"{filepath}\nProbleem:\n{repr(e)}"]
        except OSError as e:
            return [f"Er is een fout opgetreden bij het openen van het "
                    f"bestand:\n{filepath}\nProbleem:\n{repr(e)}"]
        except KeyError as e:
            return [f"Een of meer parameters missen. Bestand:\
            n{filepath}\nProbleem:\n{repr(e)}"]
        except ValueError as e:
            return [f"Dit bestand bevat geen geldige project "
                    f"instellingen:\n{filepath}\nProbleem:\n{repr(e)}"]

"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University
(Department of Information and Computing Sciences)
"""
