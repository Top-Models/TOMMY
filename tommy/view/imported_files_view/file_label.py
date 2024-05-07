from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QMouseEvent
from PySide6.QtWidgets import QLabel, QSizePolicy

from tommy.controller.file_import.metadata import Metadata
from tommy.support.constant_variables import (
    heading_font, label_height,
    text_font, medium_light_gray, hover_medium_light_gray,
    pressed_medium_light_gray)


class FileLabel(QLabel):
    """A class to formulate the FileLabel object."""

    clicked = Signal(object)

    def __init__(self, file_metadata: Metadata, parent=None) -> None:
        """Method to initialize the FileLabel object"""
        super().__init__(file_metadata.name, parent)
        self.file = file_metadata

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


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University 
(Department of Information and Computing Sciences)
"""
