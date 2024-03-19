from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QMouseEvent
from PySide6.QtWidgets import QLabel, QSizePolicy

from tommy.controller.file_import.metadata import Metadata
from tommy.support.constant_variables import (
    heading_font,
    sec_col_orange,
    hover_seco_col_orange,
    pressed_seco_col_orange,
    text_font)
from tommy.view.observer.observer import Observer


class FileLabel(QLabel, Observer):
    """A class to formulate the FileLabel object."""

    clicked = Signal(object)

    def __init__(self, file: Metadata, parent=None) -> None:
        """Method to initialize the FileLabel object"""
        super().__init__(file.name, parent)
        self.file = file

        if file.title is not None:
            self.setText(file.title)
        else:
            self.setText(file.name)

        self.setStyleSheet(f"font-family: {text_font};"
                           f"font-size: 15px;"
                           f"background-color: {sec_col_orange};"
                           f"color: black;"
                           f"margin: 0px;"
                           f"padding: 10px;")
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
                               f"font-size: 15px;"
                               f"background-color: {hover_seco_col_orange};"
                               f"color: black;"
                               f"margin: 0px;"
                               f"padding: 10px;")

    def leaveEvent(self, event):
        """
        Change the style of the label when the mouse leaves.
        :param event: The mouse leave event
        :return: None
        """
        if not self.selected:
            self.setStyleSheet(f"font-family: {text_font};"
                               f"font-size: 15px;"
                               f"background-color: {sec_col_orange};"
                               f"color: black;"
                               f"margin: 0px;"
                               f"padding: 10px;")

    def mousePressEvent(self, event: QMouseEvent) -> None:
        """
        Change the style of the label when the mouse is pressed.
        :param event: The mouse press event
        :return: None
        """
        if not self.selected:
            self.selected = True
            self.setStyleSheet(f"font-family: {text_font};"
                               f"font-size: 15px;"
                               f"background-color: {pressed_seco_col_orange};"
                               f"color: black;"
                               f"margin: 0px;"
                               f"padding: 10px;")
            self.clicked.emit(self)
        super().mousePressEvent(event)

    def deselect(self) -> None:
        """
        Deselect the label
        :return: None
        """
        try:
            self.selected = False
            self.setStyleSheet(f"font-family: {text_font};"
                               f"font-size: 15px;"
                               f"background-color: {sec_col_orange};"
                               f"color: black;"
                               f"margin: 0px;"
                               f"padding: 10px;")
        except RuntimeError:
            pass

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        """
        Change the style of the label when the mouse is released
        :param event: The mouse release event
        :return: None
        """
        if not self.selected:
            self.setStyleSheet(f"font-family: {heading_font};"
                               f"font-size: 15px;"
                               f"background-color: {hover_seco_col_orange};"
                               f"color: black;"
                               f"margin: 0px;"
                               f"padding: 10px;")
        super().mouseReleaseEvent(event)

    def update_observer(self, publisher) -> None:
        """
        Update the observer.

        :param publisher: The publisher that is being observed
        :return: None
        """
        pass


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University 
(Department of Information and Computing Sciences)
"""
