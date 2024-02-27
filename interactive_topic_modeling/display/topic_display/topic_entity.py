from PySide6.QtCore import Qt
from PySide6.QtWidgets import QVBoxLayout, QLabel, QHBoxLayout, QFrame

from interactive_topic_modeling.support.constant_variables import prim_col_red, heading_font, text_font


class TopicEntity(QFrame):
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
        topic_label.setStyleSheet(f"font-family: {heading_font}; font-size: 15px;")
        topic_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(topic_label)

        # Initialize word widgets
        word_layout = QVBoxLayout()
        main_layout.addLayout(word_layout)

        # Adding words horizontally
        horizontal_layout = QHBoxLayout()
        for i, word in enumerate(topic_words):
            word_label = QLabel(word, self)
            word_label.setStyleSheet(
                f"font-family: {text_font}; "
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
