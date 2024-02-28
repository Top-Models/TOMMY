from PySide6.QtCore import Qt
from PySide6.QtWidgets import QGridLayout, QLabel, QScrollArea, QWidget


class StopwordsDisplay(QScrollArea):

    def __init__(self):
        super().__init__()

        # Initialize widget properties
        self.setStyleSheet("background-color: white;")

        # Initialize layout for scroll area
        self.scroll_area = QWidget()
        self.layout = QGridLayout(self.scroll_area)
        self.layout.setAlignment(Qt.AlignCenter)

        # Initialize excluded words
        for i in range(1, 5):
            test_label = QLabel("Word")
            test_label.setStyleSheet("background-color: pink;")
            test_label.setAlignment(Qt.AlignCenter)
            test_label.setFixedSize(200, 100)
            self.layout.addWidget(test_label)

        # Set scroll area as focal point
        self.setWidget(self.scroll_area)

        # Add scroll options
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setWidgetResizable(True)

