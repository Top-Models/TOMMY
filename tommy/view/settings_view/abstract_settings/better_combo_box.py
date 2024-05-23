from PySide6.QtCore import Qt
from PySide6.QtGui import QWheelEvent
from PySide6.QtWidgets import QComboBox


class BetterComboBox(QComboBox):
    def __init__(self):
        super().__init__()

    def wheelEvent(self, event: QWheelEvent):
        event.ignore()
