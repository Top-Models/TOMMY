from tommy.model.project_settings_model import ProjectSettingsModel


class ProjectSettingsController:
    project_settings_model: ProjectSettingsModel = None

    @staticmethod
    def set_project_settings_model(project_settings_model: ProjectSettingsModel):
        ProjectSettingsController.project_settings_model = project_settings_model


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University 
(Department of Information and Computing Sciences)
"""
