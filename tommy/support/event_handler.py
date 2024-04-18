from collections.abc import Callable


class EventHandler[T]:
    """A class for publishing an event that other classes can subscribe to"""
    def __init__(self) -> None:
        """Initialize the eventhandler with an empty list of subscribers"""
        self.subscribers: list[Callable[[T], None]] = []

    def subscribe(self, callback: Callable[[T], None]) -> None:
        """
        Subscribe a function to this event
        :callback: The callback function to be called when the event is
            triggered
        :return: None
        """
        self.subscribers.append(callback)

    def unsubscribe(self, callback: Callable[[T], None]) -> None:
        """
        Remove/unsubscribe a callback function from this event
        :callback: The callback function to be removed from this event
        :return: None
        """
        if callback in self.subscribers:
            self.subscribers.remove(callback)

    def publish(self, event_data: T) -> None:
        """
        Trigger the event and call all registered functions on the event_data
        :param event_data: The event data to supply the functions with
        :return: None
        """
        for callback in self.subscribers:
            callback(event_data)
