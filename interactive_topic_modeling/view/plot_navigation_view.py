from PySide6.QtWidgets import QTabWidget

from interactive_topic_modeling.backend.observer.publisher import Publisher
from interactive_topic_modeling.view.observer.observer import Observer


class PlotNavigationView(QTabWidget, Observer):
    """View containing buttons to navigate plots."""

    def __init__(self) -> None:
        """Initialize the PlotNavigationView."""
        super().__init__()

    def update_observer(self, publisher: Publisher) -> None:
        """
        Update the observer.

        :param publisher: The publisher that is being observed
        :return: None
        """
        pass


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University 
(Department of Information and Computing Sciences)
"""
