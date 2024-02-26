from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QGridLayout, QSizePolicy
)

from interactive_topic_modeling.display.fetched_topics_display import FetchedTopicsDisplay
from interactive_topic_modeling.display.file_stats_display import FileStatsDisplay
from interactive_topic_modeling.display.graph_display import GraphDisplay
from interactive_topic_modeling.display.imported_files_display import ImportedFilesDisplay
from interactive_topic_modeling.display.model_params_display import ModelParamsDisplay
from interactive_topic_modeling.display.stopwords_display import StopwordsDisplay
from interactive_topic_modeling.support.constant_variables import text_font


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        # Initialize window
        self.setWindowTitle("EMMA | Topic Modelling Client")
        self.setMinimumSize(QSize(800, 600))
        self.setStyleSheet("background-color: white;"
                           f"font-family: {text_font};"
                           "border-radius: 2px;"
                           "border: none;")

        # Initialize container
        container = QWidget()
        layout = QGridLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(0)  # Remove spacing between widgets
        layout.setContentsMargins(0, 0, 0, 0)
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Initialize widgets
        self.model_params_display = ModelParamsDisplay()
        self.stopwords_display = StopwordsDisplay()
        self.imported_files_display = ImportedFilesDisplay()
        self.graph_display = GraphDisplay()
        self.file_stats_display = FileStatsDisplay()
        self.fetched_topics_display = FetchedTopicsDisplay()

        # Add widgets
        layout.addWidget(self.model_params_display, 0, 0)
        layout.addWidget(self.stopwords_display, 1, 0)
        layout.addWidget(self.imported_files_display, 1, 1)
        layout.addWidget(self.graph_display, 0, 1)
        layout.addWidget(self.file_stats_display, 1, 2)
        layout.addWidget(self.fetched_topics_display, 0, 2)
