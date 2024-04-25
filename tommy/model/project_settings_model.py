import os
from typing import List

from tommy.model.config_model import ConfigModel
from tommy.model.model_parameters_model import ModelParametersModel


class ProjectSettingsModel:
    """A class representing project settings."""
    def __init__(self) -> None:
        # Set input_folder_path to "data" by default
        self.input_folder_path: str = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "data/csv_files")
        # Initialize config
        self.configs: List[ConfigModel] = [self._create_default_config()]

    def _create_default_config(self) -> ConfigModel:
        """Create a default configuration."""
        default_config = ConfigModel("Testconfig")
        default_config.model_parameters = ModelParametersModel()
        return default_config

"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University 
(Department of Information and Computing Sciences)
"""
