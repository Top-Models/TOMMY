from abc import abstractmethod

from tommy.backend.observer.publisher import Publisher


class Observer:
    """Observer class for the Observer pattern."""

    @abstractmethod
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
