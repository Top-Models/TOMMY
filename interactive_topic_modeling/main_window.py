from PySide6.QtCore import QSize
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QPushButton
)

from interactive_topic_modeling.display.graph_display import GraphDisplay
from interactive_topic_modeling.display.stopwords_display import StopwordsDisplay
from interactive_topic_modeling.display.imported_files_display.imported_files_display import ImportedFilesDisplay
from interactive_topic_modeling.display.model_params_display import ModelParamsDisplay
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
        self.imported_files_display = ImportedFilesDisplay()
        self.graph_display = GraphDisplay()

        # Create apply button
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

        # Create next plot button
        self.next_plot_button = QPushButton("Volgende plot")
        self.next_plot_button.clicked.connect(self.on_next_plot_clicked)
        self.next_plot_button.setStyleSheet(f"""
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

        # Create previous plot button
        self.previous_plot_button = QPushButton("Vorige plot")
        self.previous_plot_button.clicked.connect(self.on_previous_plot_clicked)
        self.previous_plot_button.setStyleSheet(f"""
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
        self.initialize_widget(self.model_params_display, 0, 0, 250, 300)
        # TODO: Why is stopwords_display accessed via the imported files display?
        self.initialize_widget(self.imported_files_display.stopwords_display, 0, 300, 250, 397)
        self.initialize_widget(self.imported_files_display, 250, 438, 700, 260)
        self.initialize_widget(self.imported_files_display.file_stats_display, 950, 438, 250, 260)
        self.initialize_widget(self.graph_display.fetched_topics_display, 950, 0, 250, 438)
        self.initialize_widget(self.graph_display, 250, 8, 700, 430)
        self.initialize_widget(self.apply_button, 842, 390, 100, 40)
        self.initialize_widget(self.next_plot_button, 365, 390, 100, 40)
        self.initialize_widget(self.next_plot_button, 365, 390, 100, 40)
        self.initialize_widget(self.previous_plot_button, 258, 390, 100, 40)

        # Display correct initial files
        self.imported_files_display.fetch_files(self.graph_display.get_active_tab_name())
        self.imported_files_display.display_files(self.graph_display.get_active_tab_name())

        # Connecting the tabBarClicked signal to a method in ImportedFilesDisplay
        self.graph_display.tabBarClicked.connect(
            lambda tab_index: self.imported_files_display.display_files(
                self.graph_display.tabText(tab_index))
        )

        # Connecting the tabBarClicked signal to a method in ImportedFilesDisplay
        self.graph_display.tabBarClicked.connect(
            lambda tab_index: self.imported_files_display.file_stats_display.display_no_file_selected()
        )

        # Connecting the apply button to the graph display
        self.apply_button.clicked.connect(
            self.validate_input
        )

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

    def on_next_plot_clicked(self) -> None:
        """
        Event handler for when the next plot button is clicked
        :return: None
        """
        self.graph_display.next_plot(self.graph_display.tabText(self.graph_display.currentIndex()))

    def on_previous_plot_clicked(self) -> None:
        """
        Event handler for when the previous plot button is clicked
        :return: None
        """
        self.graph_display.previous_plot(self.graph_display.tabText(self.graph_display.currentIndex()))

    def validate_input(self) -> None:
        input = self.model_params_display.fetch_topic_num()
        if 1 <= input <= 1000:
            print("correct_input")
            self.graph_display.apply_topic_modelling(
                self.imported_files_display.file_container[self.graph_display.get_active_tab_name()],
                input,
                self.imported_files_display.stopwords_display.additional_stopwords
            )
        else:
            self.model_params_display.incorrect_input()
            print("incorrect_input")