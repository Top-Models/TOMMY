import os
import sys
from dataclasses import dataclass


@dataclass
class ProjectSettings:
    """A class that holds all the data needed to rerun a project."""
    selected_folder: str = ""
    preprocessing_data_folder: str = ""
    project_name: str = "your project"


def get_standard_input_folder() -> str:
    """
    Returns: the standard location where input will be expected by the
    application Note: this is a temporary hardcoded location for now.
    """
    base_dir = get_base_dir()
    return os.path.join(base_dir, "data")


def get_preprocessing_data_folder() -> str:
    """
    Returns: the standard location where data needed for preprocessing will
    be expected by the application (such as stopwords and maybe spacy
    pipeline downloads) Note: this is a temporary hardcoded location for
    now.
    """
    base_dir = get_base_dir()
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(base_dir, "preprocessing_data")
    return os.path.join(base_dir, "backend", "preprocessing")


def get_base_dir() -> str:
    """"
    Returns: the current working directory of the project (where
    main.py is located) Note: returns location of the '_internal' directory
    in a one-dir build by pyinstaller.
    """
    return os.path.abspath(getattr(sys, '_MEIPASS', os.getcwd()))


current_project_settings = ProjectSettings(get_standard_input_folder(),
                                           get_preprocessing_data_folder())

"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University 
(Department of Information and Computing Sciences)
"""
