from PySide6.QtCore import Qt
from PySide6.QtWidgets import QVBoxLayout, QLabel, QHBoxLayout, QFrame

from interactive_topic_modeling.support.constant_variables import (
    prim_col_red, heading_font, text_font)
from interactive_topic_modeling.view.observer.observer import Observer


class TopicEntity(QFrame, Observer):
    """The TopicEntity frame that shows the topics and related words"""
    def __init__(self, topic_name: str, topic_words: list[str]) -> None:
        """
        Initialize a topic frame.

        :param topic_name: The name of the topic.
        :param topic_words: The words related to the topic.
        :return: None.
        """
        super().__init__()

        # Initialize layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Initialize widget properties
        self.setStyleSheet(f"background-color: {prim_col_red}; "
                           f"color: white;")
        self.setFixedWidth(200)

        # Initialize title widget
        self.initialize_topic_label(topic_name)

        # Initialize word widgets
        self.word_layout = QVBoxLayout()
        self.main_layout.addLayout(self.word_layout)

        # Adding words horizontally
        self.horizontal_layout = QHBoxLayout()
        self.initialize_words(topic_words)

    def initialize_topic_label(self, topic_name: str) -> None:
        """
        Initialize the topic label.

        :param topic_name: The name of the topic.
        :return: None
        """
        topic_label = QLabel(topic_name, self)
        topic_label.setStyleSheet(
            f"font-family: {heading_font}; font-size: 15px;"
            f"font-weight: bold;"
            f"text-transform: uppercase;")
        topic_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(topic_label)

    def initialize_words(self, topic_words: list[str]) -> None:
        """
        Initialize the word labels.

        :param topic_words: The words related to the topic.
        :return: None
        """
        for i, word in enumerate(topic_words):
            word_label = self.initialize_word_label(word)
            self.horizontal_layout.addWidget(word_label)

            # Go to next row after 2 words or after long word
            if (i + 1) % 2 == 0 or len(word) >= 8:
                self.word_layout.addLayout(self.horizontal_layout)
                self.horizontal_layout = QHBoxLayout()

        # Add remaining widgets if any
        if self.horizontal_layout.count() > 0:
            self.word_layout.addLayout(self.horizontal_layout)

    def initialize_word_label(self, word: str) -> QLabel:
        """
        Initialize the word label.

        :param word: The word to be shown.
        :return: The label with the word.
        """
        cleaned_word = word.replace('"', ' ')
        word_label = QLabel(cleaned_word, self)
        word_label.setStyleSheet(f"font-family: {text_font}; font-size: 12px; "
                                 f"background-color: white; padding: 10px; "
                                 f"color: black")
        word_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        return word_label

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
