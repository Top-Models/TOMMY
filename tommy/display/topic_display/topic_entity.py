from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QVBoxLayout, QLabel, QHBoxLayout, QFrame

from tommy.support.constant_variables import prim_col_red, heading_font, text_font


class TopicEntity(QFrame):
    wordClicked = Signal(str)

    def __init__(self, topic_name: str, topic_words: list[str]):
        super().__init__()

        # Initialize layout
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Initialize widget properties
        self.setStyleSheet(f"background-color: {prim_col_red}; color: white;")
        self.setFixedWidth(200)

        # Initialize title widget
        topic_label = QLabel(topic_name, self)
        topic_label.setStyleSheet(f"font-family: {heading_font}; font-size: 15px;"
                                  f"font-weight: bold;"
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
        for i, word in enumerate(topic_words):
            cleaned_word = word.replace('"', ' ')
            word_label = QLabel(cleaned_word, self)
            word_label.setStyleSheet(
                f"font-family: {text_font}; "
                f"font-size: 12px; "
                f"background-color: white; "
                f"padding: 10px; "
                f"color: black")
            word_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            word_label.setCursor(Qt.CursorShape.PointingHandCursor)  # Set cursor to pointing hand
            word_label.mousePressEvent = lambda event, w=word_label: self.on_word_clicked(w.text())  # Connect click event
            horizontal_layout.addWidget(word_label)

            # Add word label to list
            self.word_labels.append(word_label)

            # Go to next row after 2 words or after long word
            if (i + 1) % 2 == 0 or len(word) >= 8:
                self.word_layout.addLayout(horizontal_layout)
                horizontal_layout = QHBoxLayout()

        # Add remaining widgets if any
        if horizontal_layout.count() > 0:
            self.word_layout.addLayout(horizontal_layout)

    def on_word_clicked(self, word: str):
        self.wordClicked.emit(word)

    def change_word_style(self, word: str, background_color: str, text_color: str):
        for word_label in self.word_labels:
            if word_label.text() == word:
                word_label.setStyleSheet(
                    f"font-family: {text_font}; "
                    f"font-size: 12px; "
                    f"background-color: {background_color}; "
                    f"padding: 10px; "
                    f"color: {text_color}")
            else:
                word_label.setStyleSheet(
                    f"font-family: {text_font}; "
                    f"font-size: 12px; "
                    f"background-color: white; "
                    f"padding: 10px; "
                    f"color: black")
