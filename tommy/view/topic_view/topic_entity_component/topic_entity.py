from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (QVBoxLayout, QHBoxLayout, QFrame,
                               QLineEdit, QRadioButton)

from tommy.support.constant_variables import (
    heading_font, text_font, sec_col_purple, pressed_seco_col_purple,
    seco_purple_border_color, hover_seco_col_purple)
from tommy.view.topic_view.topic_entity_component.word_entity import WordEntity


class TopicEntity(QFrame):
    """
    A class representing a topic.
    """

    wordClicked = Signal(str)
    clicked = Signal(object)

    def __init__(self,
                 topic_name: str,
                 topic_words: list[str],
                 index: int):
        """
        Initialize a topic frame.

        :param topic_name: The name of the topic.
        :param topic_words: The words related to the topic.
        :return: None.
        """
        super().__init__()
        self.topic_name = topic_name
        self.topic_words = topic_words
        self.index = index
        self.word_entities = []
        self.selected = False

        # Initialize layout
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignTop |
                                 Qt.AlignmentFlag.AlignHCenter)
        main_layout.setContentsMargins(5, 5, 5, 5)  # Adjust margins as needed
        main_layout.setSpacing(5)  # Adjust spacing as needed

        # Initialize widget properties
        self.setStyleSheet(f"background-color: {sec_col_purple};")
        self.setFixedWidth(150)

        # Initialize radio button layout
        radio_layout = QHBoxLayout()
        radio_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        radio_layout.setContentsMargins(0, 0, 0, 0)

        # Initialize radio button
        self.radio_button = QRadioButton(self)
        radio_layout.addWidget(self.radio_button)
        main_layout.addLayout(radio_layout)
        self.radio_button.clicked.connect(
            lambda checked: self.clicked.emit(self))

        # Initialize title widget
        self.topic_label = QLineEdit(topic_name, self)
        self.topic_label.setStyleSheet(f"font-family: {heading_font}; "
                                       f"color: white;"
                                       f"font-size: 15px; "
                                       f"font-weight: bold; "
                                       f"background-color: "
                                       f"{pressed_seco_col_purple};"
                                       f"padding: 5px 5px;"
                                       f"border-radius: 2px;"
                                       f"border:"
                                       f"2px solid {seco_purple_border_color};"
                                       )
        self.topic_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.topic_label.setPlaceholderText(topic_name)
        main_layout.addWidget(self.topic_label)

        # Initialize word widgets
        self.word_layout = QVBoxLayout()
        main_layout.addLayout(self.word_layout)

        # List to store word labels
        self.word_labels = []

        # Adding words horizontally
        horizontal_layout = QVBoxLayout()
        self.add_words(horizontal_layout, topic_words)

        # Add remaining widgets if any
        if horizontal_layout.count() > 0:
            self.word_layout.addLayout(horizontal_layout)

        self.topic_label.textChanged.connect(self.get_topic_name)

    def get_topic_name(self) -> str:
        """
        Get the topic name

        :return: The topic name
        """
        return self.topic_label.text()

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

    def mousePressEvent(self, event):
        """
        Emit signal when topic is clicked.
        :param event: The mouse press event
        :return: None
        """
        self.clicked.emit(self)

    def select(self) -> None:
        """
        Select the label.

        :return: None
        """
        self.selected = True
        self.radio_button.setChecked(True)
        self.setStyleSheet(f"background-color: {pressed_seco_col_purple}; "
                           f"color: white;")

    def deselect(self) -> None:
        """
        Deselect the label.

        :return: None
        """
        self.selected = False
        self.radio_button.setChecked(False)
        self.setStyleSheet(f"background-color: {sec_col_purple}; "
                           f"color: white;")

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
            if word_entity.toPlainText() == word:
                word_entity.selected = True
                word_entity.setStyleSheet(
                    f"font-family: {text_font}; "
                    f"font-size: 12px; "
                    f"background-color: {background_color}; "
                    f"color: {text_color}")
            else:
                word_entity.selected = False
                word_entity.setStyleSheet(
                    f"font-family: {text_font}; "
                    f"font-size: 12px; "
                    f"background-color: white; "
                    f"color: black")


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University
(Department of Information and Computing Sciences)
"""
