from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QMouseEvent, QPainter, QColor
from PySide6.QtWidgets import QLabel, QSizePolicy

from tommy.controller.file_import.metadata import Metadata
from tommy.support.constant_variables import (
    heading_font, label_height,
    text_font, medium_light_gray, hover_medium_light_gray,
    pressed_medium_light_gray, seco_col_blue)


class FileLabel(QLabel):
    """A class to formulate the FileLabel object."""

    clicked = Signal(object)

    def __init__(self, file_metadata: Metadata, parent=None,
                 topic_correspondence: float = None) -> None:
        """
        Method to initialize the FileLabel object
        :param file_metadata: The metadata of a file
        :param parent: The QT parent
        :param topic_correspondence: optional correspondence with topic
        """

        super().__init__(file_metadata.name, parent)
        self.file = file_metadata
        self.topic_correspondence = topic_correspondence

        if file_metadata.title is not None:
            self.setText(file_metadata.title)
        else:
            self.setText(file_metadata.name)

        self.setMaximumHeight(label_height)
        self.setStyleSheet(f"font-family: {text_font};"
                           f"font-size: 12px;"
                           f"background-color: {medium_light_gray};"
                           f"color: black;"
                           f"margin: 0px;"
                           f"padding: 3px;")
        self.setAlignment(Qt.AlignmentFlag.AlignLeft |
                          Qt.AlignmentFlag.AlignTop)
        self.setSizePolicy(QSizePolicy.Policy.Expanding,
                           QSizePolicy.Policy.Preferred)
        self.selected = False

        # If provided, set the correspondence with the current selected topic
        if topic_correspondence is not None:
            self.setText(f"{str(100 * topic_correspondence)[:4]}% - "
                         f"{self.file.name}")

    def enterEvent(self, event):
        """
        Change the style of the label when the mouse enters.
        :param event: The mouse enter event
        :return: None
        """
        if not self.selected:
            self.setStyleSheet(f"font-family: {text_font};"
                               f"font-size: 12px;"
                               f"background-color: "
                               f"{hover_medium_light_gray};"
                               f"color: black;"
                               f"margin: 0px;"
                               f"padding: 3px;")

    def leaveEvent(self, event):
        """
        Change the style of the label when the mouse leaves.
        :param event: The mouse leave event
        :return: None
        """
        if not self.selected:
            self.setStyleSheet(f"font-family: {text_font};"
                               f"font-size: 12px;"
                               f"background-color: {medium_light_gray};"
                               f"color: black;"
                               f"margin: 0px;"
                               f"padding: 3px;")

    def mousePressEvent(self, event: QMouseEvent) -> None:
        """
        Change the style of the label when the mouse is pressed.
        :param event: The mouse press event
        :return: None
        """
        if not self.selected:
            self.setStyleSheet(f"font-family: {text_font};"
                               f"font-size: 12px;"
                               f"background-color: "
                               f"{pressed_medium_light_gray};"
                               f"color: black;"
                               f"margin: 0px;"
                               f"padding: 3px;")
        else:
            self.deselect()

        super().mousePressEvent(event)

    def deselect(self) -> None:
        """
        Deselect the label
        :return: None
        """
        try:
            self.selected = False
            self.setStyleSheet(f"font-family: {text_font};"
                               f"font-size: 12px;"
                               f"background-color: {medium_light_gray};"
                               f"color: black;"
                               f"margin: 0px;"
                               f"padding: 3px;")
        except RuntimeError:
            pass

    def select(self) -> None:
        """
        Select the label
        :return: None
        """
        try:
            self.selected = True
            self.setStyleSheet(f"font-family: {text_font};"
                               f"font-size: 12px;"
                               f"background-color: "
                               f"{pressed_medium_light_gray};"
                               f"color: black;"
                               f"margin: 0px;"
                               f"padding: 3px;")
        except RuntimeError:
            pass

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        """
        Change the style of the label when the mouse is released
        :param event: The mouse release event
        :return: None
        """
        if not self.selected:
            self.setStyleSheet(f"font-family: {text_font};"
                               f"font-size: 12px;"
                               f"background-color: {hover_medium_light_gray};"
                               f"color: black;"
                               f"margin: 0px;"
                               f"padding: 3px;")
        self.clicked.emit(self)
        super().mouseReleaseEvent(event)

    def paintEvent(self, event) -> None:
        """
        Add a green bar to the label, sized to the document topic correspondence
        :param event: The paint event
        :return: None
        """
        super().paintEvent(event)
        if self.topic_correspondence is not None:
            painter = QPainter(self)
            bar_width = int(self.width() * self.topic_correspondence)
            bar_height = 7
            painter.fillRect(0, self.height() - bar_height, bar_width,
                             bar_height, QColor(seco_col_blue))
            painter.end()


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University
(Department of Information and Computing Sciences)
"""
