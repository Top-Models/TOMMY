import os


class ProjectSettingsModel:
    # temporarily set input_folder_path to "data" by default
    input_folder_path: str = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), "data/pdf_files")

    def __init__(self) -> None:
        pass


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University 
(Department of Information and Computing Sciences)
"""
