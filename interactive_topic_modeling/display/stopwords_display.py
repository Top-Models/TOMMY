from PySide6.QtCore import Qt
from PySide6.QtWidgets import QGridLayout, QLabel, QScrollArea, QWidget, QVBoxLayout, QLineEdit


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
        self.input_field.setPlaceholderText("Exclude word")
        self.input_field.setStyleSheet("border: 2px solid #E40046;"
                                       "background-color: white;")
        self.input_field.setFixedWidth(208)
        self.input_layout.addWidget(self.input_field)
        self.container_layout.addWidget(self.input_container)

        # Initialize scroll area and its layout
        self.scroll_area = QWidget()
        self.scroll_layout = QGridLayout(self.scroll_area)
        self.scroll_layout.setAlignment(Qt.AlignCenter)

        # Initialize excluded words
        self.show_excluded_words(25)

        # Add scroll area to container
        self.container_layout.addWidget(self.scroll_area)

        # Set container as focal point

        self.setWidget(self.container)

        # Add scroll options
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setWidgetResizable(True)

    def show_excluded_words(self, words: int):
        """
        NOTE: This function right now takes and integer of words, could be changed to a list later

        Initialize and add word labels to the scroll area
        :param words: The number of words needed to be showed
        :return: None
        """
        word_num = words

        for i in range(word_num):
            # Make and format word
            test_label = QLabel("Word {}".format(i + 1))
            test_label.setStyleSheet("background-color: #00968F;"
                                     "color: white;")
            test_label.setAlignment(Qt.AlignCenter)
            test_label.setFixedSize(100, 50)

            # Calculate placement
            row = i // 2
            col = i % 2

            # Add to layout at the right spot
            self.scroll_layout.addWidget(test_label, row, col)
