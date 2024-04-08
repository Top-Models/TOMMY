from PySide6.QtCore import Signal
from PySide6.QtWidgets import QLabel

from tommy.support.constant_variables import text_font, \
    pressed_medium_light_gray


class WordEntity(QLabel):
    """
    A class representing a word within a topic.
    """

    clicked = Signal(str)

    def __init__(self, word: str, parent):
        super().__init__(word)
        self.word = word
        self.parent = parent
        self.setStyleSheet(f"font-family: {text_font}; "
                           f"font-size: 12px; "
                           f"background-color: white; "
                           f"padding: 10px; "
                           f"color: black")

        self.selected = False

    def enterEvent(self, event) -> None:
        """
        Change the style of the word when entered

        :param event: The mouse enter event
        :return: None
        """
        if not self.selected:
            self.setStyleSheet(f"font-family: {text_font}; "
                               f"font-size: 12px; "
                               f"background-color: lightgray; "
                               f"padding: 10px; "
                               f"color: black")

    def leaveEvent(self, event) -> None:
        """
        Change the style of the word when left

        :param event: The mouse leave event
        :return: None
        """
        if not self.selected:
            self.setStyleSheet(f"font-family: {text_font}; "
                               f"font-size: 12px; "
                               f"background-color: white; "
                               f"padding: 10px; "
                               f"color: black")

    def mousePressEvent(self, event) -> None:
        """
        Emit signal when word is clicked

        :param event: The mouse press event
        :return: None
        """
        self.setStyleSheet(f"font-family: {text_font}; "
                           f"font-size: 12px; "
                           f"background-color: {pressed_medium_light_gray}; "
                           f"padding: 10px; "
                           f"color: black")

    def mouseReleaseEvent(self, event) -> None:
        """
        Emit signal when word is released

        :param event: The mouse release event
        :return: None
        """
        self.parent.wordClicked.emit(self.word)


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University 
(Department of Information and Computing Sciences)
"""
