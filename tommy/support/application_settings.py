import os
import sys
from dataclasses import dataclass


@dataclass
class ApplicationSettings:
    """A class that holds the application-wide settings."""
    preprocessing_data_folder: str


def get_standard_input_folder() -> str:
    """
    Returns the standard location where input files will be expected
    Note: this is a temporary hardcoded location for now.
    :return: the standard location where input will be expected by the
        application
    """
    base_dir = get_base_dir()
    return os.path.join(base_dir, "data")


def get_preprocessing_data_folder() -> str:
    """
    Returns the standard location where preprocessing data is stored
    :return: the standard location where data needed for preprocessing will
        be expected by the application (such as stopwords and maybe spacy
        pipeline downloads) Note: this is a temporary hardcoded location for
        now.
    """
    base_dir = get_base_dir()
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(base_dir, "preprocessing_data")
    return get_standard_input_folder()


def get_base_dir() -> str:
    """
    Returns the current working directory
    :return: the current working directory of the project (where
        main.py is located) Note: returns location of the '_internal' directory
        in a one-dir build by pyinstaller.
    """
    return os.path.abspath(getattr(sys, '_MEIPASS', os.getcwd()))


current_project_settings = ApplicationSettings(get_preprocessing_data_folder())

"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University 
(Department of Information and Computing Sciences)
"""
