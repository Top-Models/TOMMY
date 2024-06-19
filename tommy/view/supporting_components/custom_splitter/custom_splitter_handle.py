from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPainter, QFont
from PySide6.QtWidgets import QSplitterHandle


class CustomSplitterHandle(QSplitterHandle):
    """Custom splitter handle to add visual indicator."""

    def __init__(self, orientation, parent):
        super().__init__(orientation, parent)

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        font = QFont()
        font.setPointSize(25)
        painter.setFont(font)
        painter.setPen(QColor(150, 150, 150))
        if self.orientation() == Qt.Horizontal:
            painter.drawText(self.rect(), Qt.AlignCenter, "⋮")
        else:
            painter.drawText(self.rect(), Qt.AlignCenter, "⋯")
        painter.end()


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University
(Department of Information and Computing Sciences)
"""
