from tommy.model.model import Model
from typing import List


class SaveController:

    def __init__(self) -> None:
        pass

    def get_models(self) -> List[Model]:
        """
        Returns a list of the models in the current save.
        note: dummy implementation for now that only returns one new model.
        """
        return [Model()]


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University
(Department of Information and Computing Sciences)
"""
