from tommy.model.project_settings_model import ProjectSettingsModel


class ProjectSettingsController:
    project_settings_model: ProjectSettingsModel = None

    @staticmethod
    def set_project_settings_model(
            project_settings_model: ProjectSettingsModel) -> None:
        """
        Sets the reference to the project settings model

        :param project_settings_model: The project settings model
        :return: None
        """
        ProjectSettingsController.project_settings_model = (
            project_settings_model)

    @staticmethod
    def set_input_folder_path(path: str) -> None:
        """
        Set the input folder in the project settings model
        :param path: The path to set
        :return: None
        """
        ProjectSettingsController.project_settings_model.input_folder_path = (
            path)

    @staticmethod
    def get_input_folder_path() -> str:
        """
        Get the input folder from the project settings model
        :return: str: the path to the input folder
        """
        return (ProjectSettingsController.project_settings_model.
                input_folder_path)


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University 
(Department of Information and Computing Sciences)
"""
