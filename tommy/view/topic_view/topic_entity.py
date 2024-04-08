from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QVBoxLayout, QLabel, QHBoxLayout, QFrame

from tommy.support.constant_variables import heading_font, \
    text_font, sec_col_purple, label_height


class TopicEntity(QFrame):
    wordClicked = Signal(str)

    def __init__(self, topic_name: str, topic_words: list[str]):
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

        # Adding words horizontally
        horizontal_layout = QHBoxLayout()
        self.add_words(horizontal_layout, topic_words)

        # Add remaining widgets if any
        if horizontal_layout.count() > 0:
            self.word_layout.addLayout(horizontal_layout)

    def add_words(self,
                  horizontal_layout: QHBoxLayout,
                  topic_words: list[str]) -> None:
        """
        Add words to the layout
        :param horizontal_layout: The layout to add the words
        :param topic_words: Topic words to add
        :return: None
        """
        for i, word in enumerate(topic_words):
            cleaned_word = word.replace('"', ' ')
            word_label = QLabel(cleaned_word, self)
            word_label.setMaximumHeight(label_height)
            print(word_label.height())
            word_label.setStyleSheet(
                f"font-family: {text_font}; "
                f"font-size: 12px; "
                f"background-color: white; "
                f"padding: 3px; "
                f"color: black")
            word_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            word_label.setCursor(Qt.CursorShape.PointingHandCursor)
            word_label.mousePressEvent = \
                lambda event, w=word_label: self.on_word_clicked(w.text())
            horizontal_layout.addWidget(word_label)

            # Add word label to list
            self.word_labels.append(word_label)

            # Go to next row after 2 words or after long word
            if (i + 1) % 2 == 0 or len(word) >= 8:
                self.word_layout.addLayout(horizontal_layout)
                horizontal_layout = QHBoxLayout()

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
