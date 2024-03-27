from tommy.controller.publisher.publisher import Publisher
from tommy.model.project_settings_model import ProjectSettingsModel


class ProjectSettingsController(Publisher):
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
