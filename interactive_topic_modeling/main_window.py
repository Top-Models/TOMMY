from PySide6.QtCore import QSize, QPoint, Qt
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout
)

from interactive_topic_modeling.display.graph_display import GraphDisplay


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        # Initialize window
        self.setWindowTitle("EMMA | Topic Modelling Client")
        self.setMinimumSize(QSize(800, 600))
        self.setStyleSheet("background-color: white;")

        # Initialize container
        container = QWidget()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Add widgets
        graph_display = GraphDisplay()
        layout.addWidget(graph_display)

