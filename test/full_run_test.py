import pytest
from unittest.mock import patch

from PySide6 import QtCore
from PySide6.QtCore import Signal

from tommy.controller.controller import Controller


@pytest.fixture
def controller() -> Controller:
    return Controller()


class BlockingWorker(QtCore.QObject):
    """
    Mocked async worker, so the tests don't run async.
    """
    finished = Signal()

    def __init__(self, func):
        super().__init__()
        self.func = func

    def start(self):
        self.func()
        self.finished.emit()


def test_run_without_error(controller: Controller) -> None:
    with patch('tommy.controller.topic_modelling_controller.Worker',
               new=BlockingWorker):
        # test if topic modelling can run without error
        controller.project_settings_controller.set_input_folder_path(
            "../test/test_data/test_pdf_files/correct_files")
        controller.topic_modelling_controller.train_model()
        assert controller.graph_controller.has_topic_runner is True
