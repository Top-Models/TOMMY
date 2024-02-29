from dataclasses import dataclass


# This class holds all the data needed to rerun a project.
@dataclass
class ProjectSettings:
    selected_folder: str
    project_name: str = "your project"


current_project_settings = ProjectSettings("")
