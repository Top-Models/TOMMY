from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QVBoxLayout, QLabel, QHBoxLayout, QFrame

from tommy.support.constant_variables import (
    heading_font, text_font, sec_col_purple, pressed_seco_col_purple,
    hover_seco_col_purple)
from tommy.view.imported_files_view.word_entity import WordEntity


class TopicEntity(QFrame):
    """
    A class representing a topic.
    """

    wordClicked = Signal(str)
    clicked = Signal(object)

    def __init__(self, topic_name: str, topic_words: list[str]):
        super().__init__()
        self.topic_name = topic_name
        self.topic_words = topic_words

        # Initialize layout
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Initialize widget properties
        self.setStyleSheet(f"background-color: {sec_col_purple}; "
                           f"color: white;")
        self.setFixedWidth(200)

        # Initialize title widget
        topic_label = QLabel(topic_name, self)
        topic_label.setStyleSheet(f"font-family: {heading_font}; "
                                  f"font-size: 15px; "
                                  f"font-weight: bold; "
                                  f"text-transform: uppercase;")
        topic_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(topic_label)

        # Initialize word widgets
        self.word_layout = QVBoxLayout()
        main_layout.addLayout(self.word_layout)

        # List to store word labels
        self.word_entities = []

        # Adding words vertically
        vertical_word_layout = QVBoxLayout()
        self.add_words(vertical_word_layout, topic_words)

        # Add remaining widgets if any
        if vertical_word_layout.count() > 0:
            self.word_layout.addLayout(vertical_word_layout)

        self.selected = False

    def add_words(self,
                  layout: QHBoxLayout,
                  topic_words: list[str]) -> None:
        """
        Add words to the layout.

        :param layout: The layout to add the words
        :param topic_words: Topic words to add
        :return: None
        """
        for i, word in enumerate(topic_words):
            cleaned_word = word.replace('"', ' ')
            word_entity = WordEntity(cleaned_word)
            word_entity.clicked.connect(self.wordClicked.emit)

            # Add word label to list
            self.word_entities.append(word_entity)

            # Add word label to layout
            layout.addWidget(word_entity)

    def enterEvent(self, event) -> None:
        """
        Change the style of the label when the mouse enters.

        :param event: The mouse enter event
        :return: None
        """
        if not self.selected:
            self.setStyleSheet(f"background-color: {hover_seco_col_purple}; "
                               f"color: white;")

    def leaveEvent(self, event) -> None:
        """
        Change the style of the label when the mouse leaves.

        :param event: The mouse leave event
        :return: None
        """
        if not self.selected:
            self.setStyleSheet(f"background-color: {sec_col_purple}; "
                               f"color: white;")

    def select(self) -> None:
        """
        Select the label.

        :return: None
        """
        self.selected = True
        self.setStyleSheet(f"background-color: {pressed_seco_col_purple}; "
                           f"color: white;")

    def deselect(self) -> None:
        """
        Deselect the label.

        :return: None
        """
        self.selected = False
        self.setStyleSheet(f"background-color: {hover_seco_col_purple}; "
                           f"color: white;")

    def mousePressEvent(self, event) -> None:
        """
        Change the style of the label when the mouse is pressed.

        :param event: The mouse press event
        :return: None
        """
        self.setStyleSheet(f"background-color: {pressed_seco_col_purple}; ")

    def mouseReleaseEvent(self, event) -> None:
        """
        Change the style of the label when the mouse is released.

        :param event: The mouse release event
        :return: None
        """
        self.clicked.emit(self)

    def change_word_style(self,
                          word: str,
                          background_color: str,
                          text_color: str) -> None:
        """
        Change the style of a word.

        :param word: The word to be changed
        :param background_color: The new background color
        :param text_color: The new text color
        :return: None
        """
        for word_entity in self.word_entities:
            if word_entity.text() == word:
                word_entity.selected = True
                word_entity.setStyleSheet(
                    f"font-family: {text_font}; "
                    f"font-size: 12px; "
                    f"background-color: {background_color}; "
                    f"padding: 10px; "
                    f"color: {text_color}")
            else:
                word_entity.selected = False
                word_entity.setStyleSheet(
                    f"font-family: {text_font}; "
                    f"font-size: 12px; "
                    f"background-color: white; "
                    f"padding: 10px; "
                    f"color: black")


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University 
(Department of Information and Computing Sciences)
"""