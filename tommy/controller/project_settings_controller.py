from tommy.model.project_settings_model import ProjectSettingsModel


class ProjectSettingsController:
    _project_settings_model: ProjectSettingsModel = None

    def __init__(self) -> None:
        pass

    def set_model_refs(self, project_settings_model: ProjectSettingsModel):
        self._project_settings_model = project_settings_model


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University 
(Department of Information and Computing Sciences)
"""
