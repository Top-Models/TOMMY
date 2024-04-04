from PySide6.QtCore import Qt
from PySide6.QtWidgets import QVBoxLayout, QLabel, QScrollArea, QLineEdit, QWidget, QHBoxLayout
from tommy.support.constant_variables import text_font, heading_font, seco_col_blue, \
    hover_seco_col_blue


class ModelParamsDisplay(QScrollArea):

    def __init__(self):
        super().__init__()

        # Initialize widget properties
        self.setStyleSheet("background-color: rgba(230, 230, 230, 230);"
                           "margin: 0px;"
                           "padding: 0px;"
                           "border-bottom: 3px solid lightgrey;")

        # Initialize layout
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        # Initialize container that will hold settings
        self.container = QWidget()
        self.container.setStyleSheet("border: none;")
        self.container_layout = QVBoxLayout(self.container)
        self.container_layout.setAlignment(Qt.AlignTop)

        # Initialize title label
        self.title_label = QLabel("Model parameters")
        self.title_label.setStyleSheet(f"font-size: 13px;"
                                       f"font-family: {heading_font};"
                                       f"font-weight: bold;"
                                       f"text-transform: uppercase;"
                                       f"background-color: {seco_col_blue};"
                                       f"color: white;"
                                       f"border-bottom: 3px solid {hover_seco_col_blue};")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)
        self.title_label.setContentsMargins(0, 0, 0, 0)
        self.title_label.setFixedHeight(50)
        self.layout.addWidget(self.title_label)

        # Initialize topic widgets
        topic_label = QLabel("Aantal topics:")
        topic_label.setStyleSheet(f"font-size: 16px;"
                                  f"color: black;"
                                  f"font-family: {text_font}")
        topic_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.container_layout.addWidget(topic_label)

        self.topic_input = QLineEdit()
        self.topic_input.setPlaceholderText("Voer aantal topics in")
        self.topic_input.setText("5")
        self.topic_input.setStyleSheet(f"border-radius: 5px;"
                                       f"font-size: 14px;"
                                       f"font-family: {text_font};"
                                       f"color: black;"
                                       f"border: 2px solid #00968F;"
                                       f"padding: 5px;"
                                       f"background-color: white;")
        self.topic_input.setAlignment(Qt.AlignLeft)
        self.container_layout.addWidget(self.topic_input)
        self.topic_input.returnPressed.connect(self.fetch_topic_num)

        # Add widgets
        self.layout.addWidget(self.container)


    def fetch_topic_num(self):
        topic_num_output = self.topic_input.text()

        try:
            topic_num = int(topic_num_output)
            # reset style
            self.topic_input.setStyleSheet(f"border-radius: 5px;"
                                           f"font-size: 14px;"
                                           f"font-family: {text_font};"
                                           f"color: black;"
                                           f"border: 2px solid #00968F;"
                                           f"padding: 5px;"
                                           f"background-color: white;")
            return topic_num
        except ValueError:
            print("Invalid input. Please enter a valid integer.")
            # 0 is handled in mainwindow
            return 0

    def incorrect_input(self) -> None:
        self.topic_input.setText("")
        self.topic_input.setPlaceholderText("Incorrect Input")
        self.topic_input.setStyleSheet(f"border-radius: 5px;"
                                       f"font-size: 14px;"
                                       f"font-family: {text_font};"
                                       f"color: black;"
                                       f"border: 4px solid red;"
                                       f"padding: 5px;"
                                       f"background-color: white;")
