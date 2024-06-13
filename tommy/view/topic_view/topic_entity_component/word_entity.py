from PySide6.QtCore import Signal
from PySide6.QtWidgets import QLabel, QTextEdit

from tommy.support.constant_variables import text_font, \
    pressed_medium_light_gray, label_height, topic_entity_word_font


class WordEntity(QTextEdit):
    """
    A class representing a word within a topic.
    """

    clicked = Signal(str)

    def __init__(self, word: str):
        super().__init__(word)
        self.word = word
        self.setStyleSheet(f"background-color: white; "
                           f"color: black")
        self.setFont(topic_entity_word_font)
        self.setContentsMargins(10, 0, 10, 0)
        self.setFixedHeight(label_height)
        self.selected = False
        self.setReadOnly(True)  # Make the QTextEdit read-only
        self.setLineWrapMode(QTextEdit.WidgetWidth)  # Enable word wrapping

    def enterEvent(self, event) -> None:
        """
        Change the style of the word when entered

        :param event: The mouse enter event
        :return: None
        """
        if not self.selected:
            self.setStyleSheet(f"background-color: lightgray; "
                               f"color: black")

    def leaveEvent(self, event) -> None:
        """
        Change the style of the word when left

        :param event: The mouse leave event
        :return: None
        """
        if not self.selected:
            self.setStyleSheet(f"background-color: white; "
                               f"color: black")

    def mousePressEvent(self, event) -> None:
        """
        Emit signal when word is clicked

        :param event: The mouse press event
        :return: None
        """
        super().mousePressEvent(event)
        self.setStyleSheet(f"background-color: {pressed_medium_light_gray}; "
                           f"color: black")

    def mouseReleaseEvent(self, event) -> None:
        """
        Emit signal when word is released

        :param event: The mouse release event
        :return: None
        """
        self.clicked.emit(self.word)


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University
(Department of Information and Computing Sciences)
"""
