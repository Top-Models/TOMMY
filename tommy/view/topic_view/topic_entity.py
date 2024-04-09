from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QVBoxLayout, QLabel, QHBoxLayout, QFrame, \
    QSizePolicy

from tommy.support.constant_variables import (
    heading_font,
    text_font,
    sec_col_purple,
    label_height)


class TopicEntity(QFrame):
    """The TopicEntity frame that shows the topics and related words"""
    wordClicked = Signal(str)

    def __init__(self, topic_name: str, topic_words: list[str]):
        """
        Initialize a topic frame.

        :param topic_name: The name of the topic.
        :param topic_words: The words related to the topic.
        :return: None.
        """
        super().__init__()

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
        self.word_labels = []

        # Adding words vertically
        vertical_layout = QVBoxLayout()
        self.add_words(vertical_layout, topic_words)

        # Add remaining widgets if any
        if vertical_layout.count() > 0:
            self.word_layout.addLayout(vertical_layout)

    def add_words(self,
                  vertical_layout: QVBoxLayout,
                  topic_words: list[str]) -> None:
        """
        Add words to the layout
        :param vertical_layout: The layout to add the words
        :param topic_words: Topic words to add
        :return: None
        """
        for i, word in enumerate(topic_words):
            cleaned_word = word.replace('"', ' ')
            word_label = QLabel(cleaned_word, self)
            word_label.setSizePolicy(QSizePolicy.Policy.Expanding,
                                     QSizePolicy.Policy.Preferred)
            word_label.setMaximumHeight(label_height)
            word_label.setStyleSheet(
                    f"font-family: {text_font}; "
                    f"font-size: 12px; "
                    f"background-color: white; "
                    f"padding: 3px; "
                    f"color: black")
            word_label.setCursor(Qt.CursorShape.PointingHandCursor)
            word_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            word_label.mousePressEvent = \
                lambda event, w=word_label: self.on_word_clicked(w.text())
            vertical_layout.addWidget(word_label)

            # Add word label to list
            self.word_labels.append(word_label)

    def on_word_clicked(self, word: str):
        """
        Emit signal when word is clicked
        :param word: The word that was clicked
        :return: None
        """
        self.wordClicked.emit(word)

    def change_word_style(self,
                          word: str,
                          background_color: str,
                          text_color: str):
        """
        Change the style of a word
        :param word: The word to be changed
        :param background_color: The new background color
        :param text_color: The new text color
        :return: None
        """
        for word_label in self.word_labels:
            if word_label.text() == word:
                word_label.setStyleSheet(
                        f"font-family: {text_font}; "
                        f"font-size: 12px; "
                        f"background-color: {background_color}; "
                        f"padding: 3px; "
                        f"color: {text_color}")
            else:
                word_label.setStyleSheet(
                        f"font-family: {text_font}; "
                        f"font-size: 12px; "
                        f"background-color: white; "
                        f"padding: 3px; "
                        f"color: black")
