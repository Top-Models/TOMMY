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
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Initialize widget properties
        self.setStyleSheet(f"background-color: {prim_col_red}; "
                           f"color: white;")
        self.setFixedWidth(200)

        # Initialize title widget
        topic_label = QLabel(topic_name, self)
        topic_label.setStyleSheet(
            f"font-family: {heading_font}; font-size: 15px;"
            f"font-weight: bold;"
            f"text-transform: uppercase;")
        topic_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(topic_label)

        # Initialize word widgets
        word_layout = QVBoxLayout()
        main_layout.addLayout(word_layout)

        # Adding words horizontally
        horizontal_layout = QHBoxLayout()
        for i, word in enumerate(topic_words):
            cleaned_word = word.replace('"', ' ')
            word_label = QLabel(cleaned_word, self)
            word_label.setStyleSheet(f"font-family: {text_font}; "
                                     f"font-size: 12px; "
                                     f"background-color: white; "
                                     f"padding: 10px; "
                                     f"color: black")
            word_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            horizontal_layout.addWidget(word_label)

            # Go to next row after 2 words or after long word
            if (i + 1) % 2 == 0 or len(word) >= 8:
                word_layout.addLayout(horizontal_layout)
                horizontal_layout = QHBoxLayout()

        # Add remaining widgets if any
        if horizontal_layout.count() > 0:
            word_layout.addLayout(horizontal_layout)

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
