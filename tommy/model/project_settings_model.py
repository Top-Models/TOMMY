class ProjectSettingsModel:
    """A class representing project settings."""

    def __init__(self) -> None:
        # Don't load anything on startup, make the user select a folder
        # themselves.
        self.input_folder_path: str = ""


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University
(Department of Information and Computing Sciences)
"""
