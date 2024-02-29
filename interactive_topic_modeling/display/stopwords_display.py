from PySide6.QtCore import Qt
from PySide6.QtWidgets import QGridLayout, QLabel, QScrollArea, QWidget, QVBoxLayout, QLineEdit, QHBoxLayout

from interactive_topic_modeling.support.constant_variables import heading_font, text_font


class StopwordsDisplay(QScrollArea):

    def __init__(self):
        super().__init__()

        # Initialize widget properties
        self.setStyleSheet("background-color: white;")

        # Initialize container for all elements
        self.container = QWidget()

        # Initialize layout for container
        self.container_layout = QVBoxLayout(self.container)
        self.container_layout.setAlignment(Qt.AlignTop)

        # Add container for the input field
        self.input_container = QWidget()
        self.input_layout = QVBoxLayout(self.input_container)
        self.input_layout.setAlignment(Qt.AlignCenter)

        # Initialize and add input field
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Woord uitsluiten:")
        self.input_field.setStyleSheet(f"border: 2px solid #E40046;"
                                       f"background-color: white;"
                                       f"font-family: {text_font};"
                                       f"margin-right: 10px;"
                                       f"color: black;")
        self.input_field.setFixedWidth(208)
        self.input_layout.addWidget(self.input_field)
        self.container_layout.addWidget(self.input_container)

        # Initialize scroll area and its layout
        self.scroll_area = QWidget()
        self.scroll_layout = QHBoxLayout(self.scroll_area)
        self.scroll_layout.setAlignment(Qt.AlignCenter)

        # Initialize excluded words
        self.word_layout = QVBoxLayout()
        self.scroll_layout.addLayout(self.word_layout)
        test_list = ["word 1", "woord 2", "woord", "ellendig woord 2", "word 1", "woord 2", "woord", "ellendig woord 2",
                     "word 1", "woord 2", "woord", "ellendig woord 2"]
        self.show_excluded_words(test_list, self.word_layout)

        # Add scroll area to container
        self.container_layout.addWidget(self.scroll_area)

        # Set container as focal point

        self.setWidget(self.container)

        # Add scroll options
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setWidgetResizable(True)

    def show_excluded_words(self, word_list: list[str], layout):
        """
        NOTE: This function right now takes and integer of words, could be changed to a list later

        Initialize and add word labels to the scroll area
        :param word_list: The list of words needed to be showed
        :return: None
        """
        horizontal_layout = QHBoxLayout()

        for i, word in enumerate(word_list):
            # Make and format word
            word_label = QLabel(word, self)
            word_label.setStyleSheet(f"background-color: #00968F;"
                                     f"color: white;"
                                     f"font-family: {text_font};"
                                     f"font-size: 12px;"
                                     f"padding: 15px;"
                                     )
            word_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            horizontal_layout.addWidget(word_label)

            if (i + 1) % 2 == 0 or len(word) >= 8:
                layout.addLayout(horizontal_layout)
                horizontal_layout = QHBoxLayout()

                # Add remaining widgets if any
            if horizontal_layout.count() > 0:
                layout.addLayout(horizontal_layout)
