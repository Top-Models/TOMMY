
class Publisher:
    """Publisher class for the Observer pattern."""

    def __init__(self):
        self.observers = []

    def add(self, observer) -> None:
        """
        Add an observer to the list of observers.
        :param observer: The observer to add
        :return: None
        """
        self.observers.append(observer)

    def remove(self, observer) -> None:
        """
        Remove an observer from the list of observers.
        :param observer: The observer to remove
        :return: None
        """
        self.observers.remove(observer)

    def notify(self) -> None:
        """
        Notify all observers.
        :return: None
        """
        [o.update_observer(self) for o in self.observers]


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University 
(Department of Information and Computing Sciences)
"""
