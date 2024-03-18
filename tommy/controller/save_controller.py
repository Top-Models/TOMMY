from tommy.model.model import Model


class SaveController:
    model: Model = None

    @staticmethod
    def set_model(model: Model):
        SaveController.model = model


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University 
(Department of Information and Computing Sciences)
"""
