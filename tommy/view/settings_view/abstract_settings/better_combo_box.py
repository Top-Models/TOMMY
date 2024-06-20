from PySide6.QtCore import Qt
from PySide6.QtGui import QWheelEvent
from PySide6.QtWidgets import QComboBox


class BetterComboBox(QComboBox):
    def __init__(self):
        super().__init__()

    def wheelEvent(self, event: QWheelEvent):
        event.ignore()

    def set_current_text_without_signal(self, text: str):
        """
        Set the current text of the combo box without emitting the index
        changed signal
        :param text:
        :return:
        """
        self.blockSignals(True)
        self.setCurrentText(text)
        self.blockSignals(False)

"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University
(Department of Information and Computing Sciences)
"""
