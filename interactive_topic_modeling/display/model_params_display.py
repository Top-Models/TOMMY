from PySide6.QtCore import Qt
from PySide6.QtWidgets import QVBoxLayout, QLabel, QScrollArea, QLineEdit, QWidget, QHBoxLayout
from interactive_topic_modeling.support.constant_variables import text_font, heading_font


class ModelParamsDisplay(QScrollArea):

    def __init__(self):
        super().__init__()

        # Initialize widget properties
        self.setStyleSheet("background-color: white;"
                           "margin: 0px;"
                           "padding: 0px;")

        # Initialize layout
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Initialize container that will hold settings
        self.container = QWidget()
        self.container.setStyleSheet("border: none;")
        self.container_layout = QVBoxLayout(self.container)
        self.container_layout.setAlignment(Qt.AlignTop)

        # Add header label
        header_label = QLabel("Settings")
        header_label.setStyleSheet(f"font-size: 16px;"
                                   f"font-family: {heading_font};"
                                   f"background-color: #E40046;"
                                   f"color: white;")
        header_label.setFixedSize(242, 34)
        header_label.setContentsMargins(-5, 0, 0, 0)
        header_label.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.layout.addWidget(header_label)

        # Initialize topic widgets
        topic_label = QLabel("Number of topics:")
        topic_label.setStyleSheet(f"font-size: 16px;"
                                  f"font-family: {text_font}")
        topic_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.container_layout.addWidget(topic_label)

        self.topic_input = QLineEdit()
        self.topic_input.setPlaceholderText("e.g. 1")
        self.topic_input.setStyleSheet(f"border-radius: 5px;"
                                       f"font-size: 14px;"
                                       f"font-family: {text_font};"
                                       f"color: black;"
                                       f"border: 2px solid #00968F")
        self.topic_input.setAlignment(Qt.AlignLeft)
        self.container_layout.addWidget(self.topic_input)
        self.topic_input.returnPressed.connect(self.fetch_topic_num)

        # Add widgets
        self.layout.addWidget(self.container)
        self.setStyleSheet("border-bottom: 2px solid #E40046;")

    def fetch_topic_num(self):
        topic_num = self.topic_input.text()
        print("Number of topics: ", topic_num)
