from tommy.model.model_parameters_model import ModelParametersModel


class ConfigModel:
    """A class representing the configuration."""
    def __init__(self, name: str):
        self.name = name
        self.model_parameters = ModelParametersModel()

    def to_dict(self):
        """
        Convert the configuration object to a dictionary.
        :return: Dictionary representation of the configuration
        """
        return {
            "name": self.name,
            "model_parameters": self.model_parameters.to_dict()
        }

    @classmethod
    def from_dict(cls, config_dict):
        """
        Create a ConfigModel instance from a dictionary representation.
        :param config_dict: Dictionary representation of the configuration
        :return: ConfigModel instance
        """
        name = config_dict.get("name")
        model_parameters_dict = config_dict.get("model_parameters")
        config = cls(name)
        if model_parameters_dict:
            config.model_parameters = ModelParametersModel.from_dict(
                model_parameters_dict)
        return config


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University 
(Department of Information and Computing Sciences)
"""