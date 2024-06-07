from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPainter
from PySide6.QtWidgets import QSplitterHandle


class CustomSplitterHandle(QSplitterHandle):
    """Custom splitter handle to add visual indicator."""

    def __init__(self, orientation, parent):
        super().__init__(orientation, parent)
        self.setFixedWidth(15)  # Set the width of the splitter handle

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setPen(QColor(150, 150, 150))
        painter.drawText(self.rect(), Qt.AlignCenter, "|||")
        painter.end()


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University
(Department of Information and Computing Sciences)
"""
