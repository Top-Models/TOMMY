from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel

from interactive_topic_modeling.support.constant_variables import prim_col_red, heading_font


class TopicEntity(QLabel):

    def __init__(self, topic_name: str, topic_words: list[str]):
        super().__init__()

        # Initialize widget properties
        self.setStyleSheet(f"background-color: {prim_col_red};"
                           f"font-family: {heading_font};"
                           "margin: 10px;"
                           "padding: 10px;")
        self.setFixedSize(200, 150)
        self.setText("Topic Entity")
        self.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

        # Initialize layout
        self.topic_name = topic_name
        self.topic_words = topic_words

        # Initialize widgets
        self.topic_name_label = QLabel(self.topic_name)
