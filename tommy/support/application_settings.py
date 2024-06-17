import os
import sys
from dataclasses import dataclass


@dataclass
class ApplicationSettings:
    """A class that holds the application-wide settings."""
    data_folder: str
    default_config_name: str = "Config 1"


def get_data_folder() -> str:
    """
    Returns the standard location where all software-dependent data is stored.
    :return: the standard location where data dependencies needed for several
        software components will be expected by the application.
    """
    return os.path.join(get_base_dir(), "data")


def get_assets_folder() -> str:
    """
    Returns the standard location where assets are stored
    :return: the standard location where assets are stored
    """
    if hasattr(sys, '_MEIPASS'):
        base_dir = get_base_dir()
    else:
        base_dir = os.path.dirname(get_base_dir())
    return os.path.join(base_dir, "assets")


def get_base_dir() -> str:
    """
    Returns the current working directory
    :return: the current working directory of the project (where
        main.py is located) Note: returns location of the '_internal' directory
        in a one-dir build by pyinstaller.
    """
    return os.path.abspath(getattr(sys, '_MEIPASS', os.getcwd()))


application_settings = ApplicationSettings(get_data_folder())


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University
(Department of Information and Computing Sciences)
"""
