from collections.abc import Callable


class EventHandler[T]:
    def __init__(self) -> None:
        self.subscribers: list[Callable[[T], None]] = []

    def subscribe(self, callback: Callable[[T], None]) -> None:
        self.subscribers.append(callback)

    def unsubscribe(self, callback: Callable[[T], None]) -> None:
        if callback in self.subscribers:
            self.subscribers.remove(callback)

    def publish(self, event_data: T) -> None:
        for callback in self.subscribers:
            callback(event_data)
