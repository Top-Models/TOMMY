import os
from dataclasses import dataclass


# This class holds all the data needed to rerun a project.
@dataclass
class ProjectSettings:
    # Set the data folder within interactive-topic-modelling/backend as selected folder
    selected_folder: str = ""
    project_name: str = "your project"


current_project_settings = ProjectSettings(os.path.join(os.path.dirname(os.path.dirname(__file__)), "data"))
