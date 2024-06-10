from tommy.support.application_settings import get_standard_input_folder


class ProjectSettingsModel:
    """A class representing project settings."""

    def __init__(self) -> None:
        # Set input_folder_path to "data" by default
        self.input_folder_path: str = get_standard_input_folder()


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University
(Department of Information and Computing Sciences)
"""
