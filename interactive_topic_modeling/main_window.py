from PySide6.QtCore import QSize
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QPushButton
)

from interactive_topic_modeling.display.topic_display.fetched_topics_display import FetchedTopicsDisplay
from interactive_topic_modeling.display.file_stats_display import FileStatsDisplay
from interactive_topic_modeling.display.graph_display import GraphDisplay
from interactive_topic_modeling.display.imported_files_display import ImportedFilesDisplay
from interactive_topic_modeling.display.model_params_display import ModelParamsDisplay
from interactive_topic_modeling.display.stopwords_display import StopwordsDisplay
from interactive_topic_modeling.support.constant_variables import text_font, seco_col_blue, hover_seco_col_blue, \
    pressed_seco_col_blue


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        # Initialize window
        self.setWindowTitle("EMMA | Topic Modelling Client")
        self.setFixedSize(QSize(1200, 700))
        self.setStyleSheet("background-color: white;"
                           "font-size: 15px;"
                           f"font-family: {text_font};"
                           "border: none;")

        # Create widgets
        self.model_params_display = ModelParamsDisplay()
        self.stopwords_display = StopwordsDisplay()
        self.imported_files_display = ImportedFilesDisplay()
        self.graph_display = GraphDisplay()
        self.file_stats_display = FileStatsDisplay()
        self.fetched_topics_display = FetchedTopicsDisplay()
        self.apply_button = QPushButton("Toepassen")
        self.apply_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {seco_col_blue};
                color: white;
            }}
            
            QPushButton:hover {{
                background-color: {hover_seco_col_blue};
            }}
            
            QPushButton:pressed {{
                background-color: {pressed_seco_col_blue};
            }}
        """)

        # Initialize widgets
        self.initialize_widget(self.model_params_display, 0, 0, 250, 350)
        self.initialize_widget(self.stopwords_display, 0, 350, 250, 350)
        self.initialize_widget(self.imported_files_display, 250, 438, 700, 275)
        self.initialize_widget(self.file_stats_display, 950, 450, 250, 250)
        self.initialize_widget(self.fetched_topics_display, 950, 0, 250, 450)
        self.initialize_widget(self.graph_display, 250, 8, 700, 430)
        self.initialize_widget(self.apply_button, 842, 390, 100, 40)


    def initialize_widget(self, widget: QWidget, x: int, y: int, w: int, h: int) -> None:
        """
        Initialize a widget on the main window.
        :param widget: The widget to initialize
        :param x: The x-coordinate of the widget
        :param y: The y-coordinate of the widget
        :param w: The width of the widget
        :param h: The height of the widget
        :return: None
        """

        widget.setParent(self)
        widget.setGeometry(x, y, w, h)
        widget.show()
