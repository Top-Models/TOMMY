from tommy.model.model_parameters_model import ModelParametersModel


class ConfigModel:
    """A class representing the configuration."""
    def __init__(self, name: str):
        self.name = name
        self.model_parameters = ModelParametersModel()

"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University 
(Department of Information and Computing Sciences)
"""