from PySide6.QtCore import QThread, Signal


class Worker(QThread):
    """
    Worker class that runs a function in a separate thread.
    Pass a function to run in __init__
    Add a callback with finished.connect()
    """
    finished = Signal()  # connect callbacks to this signal

    def __init__(self, func) -> None:
        """
        Initialize the worker with a function to run.
        :param func: The function to run async
        """
        super().__init__()
        self.func = func

    def run(self) -> None:
        """
        Virtual override running the function.
        :return:
        """
        self.func()


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University
(Department of Information and Computing Sciences)
"""
