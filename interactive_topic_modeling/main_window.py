from PySide6.QtCore import QSize
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QPushButton
)

from interactive_topic_modeling.view.graph_view import GraphView
from interactive_topic_modeling.view.model_selection_view import (
    ModelSelectionView)
from interactive_topic_modeling.view.plot_navigation_view import (
    PlotNavigationView)
from interactive_topic_modeling.view.stopwords_view import (
    StopwordsView)
from interactive_topic_modeling.view.imported_files_view. \
    imported_files_view import ImportedFilesView
from interactive_topic_modeling.view.model_params_view import (
    ModelParamsView)
from interactive_topic_modeling.support.constant_variables import (
    text_font, seco_col_blue, hover_seco_col_blue, pressed_seco_col_blue)


class MainWindow(QMainWindow):
    """Main window class for the topic modelling application"""

    def __init__(self) -> None:
        """Initialize the main window."""
        super().__init__()

        # Initialize window
        self.setWindowTitle("EMMA | Topic Modelling Client")
        self.setFixedSize(QSize(1200, 700))
        self.setStyleSheet("background-color: white;"
                           "font-size: 15px;"
                           f"font-family: {text_font};"
                           "border: none;")

        # Create widgets
        self.stopwords_view = StopwordsView()
        self.model_params_view = ModelParamsView()
        self.model_selection_view = ModelSelectionView()
        self.imported_files_view = ImportedFilesView()
        self.graph_view = GraphView()
        self.plot_navigation_view = PlotNavigationView()

        # Initialize buttons
        self.previous_plot_button = None
        self.next_plot_button = None

        # Initialize widgets
        self.initialize_widget(self.model_params_view,
                               0, 0, 250, 300)
        self.initialize_widget(self.imported_files_view.stopwords_display,
                               0, 300, 250, 397)
        self.initialize_widget(self.imported_files_view,
                               250, 438, 700, 260)
        self.initialize_widget(self.imported_files_view.file_stats_display,
                               950, 438, 250, 260)

        # TODO: Use fetched_topics_display from main_window
        self.initialize_widget(self.graph_view.fetched_topics_display,
                               950, 0, 250, 438)
        self.initialize_widget(self.graph_view,
                               250, 8, 700, 430)
        # TODO: Initialize the plot navigation view
        # TODO: Initialize the model selection view

        self.display_correct_initial_files()
        self.initialize_buttons()
        self.initialize_event_handlers()

    def initialize_widget(self, widget: QWidget,
                          x: int, y: int, w: int, h: int) -> None:
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
        Event handler for when the next plot button is clicked.

        :return: None
        """
        self.graph_view.next_plot(self.graph_view.tabText(
            self.graph_view.currentIndex()))

    def on_previous_plot_clicked(self) -> None:
        """
        Event handler for when the previous plot button is clicked.

        :return: None
        """
        self.graph_view.previous_plot(self.graph_view.tabText(
            self.graph_view.currentIndex()))

    def display_correct_initial_files(self) -> None:
        """
        Display the correct initial files in the main window.

        :return: None
        """
        self.imported_files_view.fetch_files(
            self.graph_view.get_active_tab_name())
        self.imported_files_view.display_files(
            self.graph_view.get_active_tab_name())

    def initialize_buttons(self) -> None:
        """
        Initialize the buttons in the main window.
        :return: None
        """
        self.initialize_previous_plot_button()
        self.initialize_next_plot_button()

    def initialize_next_plot_button(self) -> None:
        """
        Initialize the next plot button in the main window.
        :return: None
        """
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

        self.initialize_widget(self.next_plot_button,
                               365, 390, 100, 40)

    def initialize_previous_plot_button(self) -> None:
        """
        Initialize the previous plot button in the main window.
        :return: None
        """
        self.previous_plot_button = QPushButton("Vorige plot")
        self.previous_plot_button.clicked.connect(
            self.on_previous_plot_clicked)
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

        self.initialize_widget(self.previous_plot_button,
                               260, 390, 100, 40)

    def initialize_event_handlers(self) -> None:
        """
        Initialize event handlers for the main window.

        :return: None
        """
        # Connecting the tabBarClicked signal to a method in
        # ImportedFilesDisplay
        self.graph_view.tabBarClicked.connect(
            lambda tab_index: self.imported_files_view.display_files(
                self.graph_view.tabText(tab_index))
        )

        # Connecting the tabBarClicked signal to a method in
        # ImportedFilesDisplay
        self.graph_view.tabBarClicked.connect(
            lambda tab_index: self.imported_files_view.file_stats_display.
            display_no_file_selected()
        )

        # TODO: Remove when init in ModelParamsView is implemented
        # Connecting the apply button to the graph view
        self.model_params_view.apply_button.clicked.connect(
            lambda: self.graph_view.apply_topic_modelling(
                self.imported_files_view.file_container[
                    self.graph_view.get_active_tab_name()],
                self.model_params_view.fetch_topic_num(),
                self.imported_files_view.stopwords_display.
                additional_stopwords
            )
        )


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University 
(Department of Information and Computing Sciences)
"""
