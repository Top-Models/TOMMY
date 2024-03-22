from tommy.model.model_parameters_model import ModelParametersModel


class GraphController:
    model_parameters_model: ModelParametersModel = None

    def __init__(self) -> None:
        pass

    def set_model_refs(self, parameters_model: ModelParametersModel):
        self.model_parameters_model = parameters_model


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University 
(Department of Information and Computing Sciences)
"""
