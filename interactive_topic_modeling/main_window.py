from PySide6.QtCore import QSize
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget
)

from interactive_topic_modeling.support.constant_variables import (
    text_font)
from interactive_topic_modeling.view.graph_view import GraphView
from interactive_topic_modeling.view.imported_files_view. \
    imported_files_view import ImportedFilesView
from interactive_topic_modeling.view.model_params_view import (
    ModelParamsView)
from interactive_topic_modeling.view.model_selection_view import (
    ModelSelectionView)
from interactive_topic_modeling.view.plot_navigation_view import (
    PlotNavigationView)
from interactive_topic_modeling.view.stopwords_view import (
    StopwordsView)


class MainWindow(QMainWindow):
    """Main window class for the topic modelling application"""

    def __init__(self) -> None:
        """Initialize the main window."""
        super().__init__()

        # Initialize window
        self.setWindowTitle("TOMMY")
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

        # Initialize widgets
        self.initialize_widget(self.model_params_view,
                               0, 0, 250, 300)
        self.initialize_widget(self.imported_files_view.stopwords_display,
                               0, 300, 250, 397)
        self.initialize_widget(self.imported_files_view,
                               250, 458, 700, 240)
        self.initialize_widget(self.imported_files_view.file_stats_display,
                               950, 458, 250, 240)

        # TODO: Use fetched_topics_display from main_window
        self.initialize_widget(self.graph_view.fetched_topics_display,
                               950, 0, 250, 458)
        self.initialize_widget(self.graph_view,
                               250, 8, 700, 400)
        self.initialize_widget(self.plot_navigation_view,
                               250, 408, 700, 50)
        # TODO: Initialize the model selection view

        self.display_correct_initial_files()
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

    # TODO: Extract method when Connector is implemented
    def on_next_plot_clicked(self) -> None:
        """
        Event handler for when the next plot button is clicked.

        :return: None
        """
        self.graph_view.next_plot(self.graph_view.tabText(
            self.graph_view.currentIndex()))

    # TODO: Extract method when Connector is implemented
    def on_previous_plot_clicked(self) -> None:
        """
        Event handler for when the previous plot button is clicked.

        :return: None
        """
        self.graph_view.previous_plot(self.graph_view.tabText(
            self.graph_view.currentIndex()))

    # TODO: Extract method when Connector is implemented
    def display_correct_initial_files(self) -> None:
        """
        Display the correct initial files in the main window.

        :return: None
        """
        self.imported_files_view.fetch_files(
            self.graph_view.get_active_tab_name())
        self.imported_files_view.display_files(
            self.graph_view.get_active_tab_name())

    # TODO: Extract method when Connector is implemented
    def initialize_event_handlers(self) -> None:
        """
        Initialize event handlers for the main window.

        :return: None
        """

        # Next plot button
        self.plot_navigation_view.next_plot_button.clicked.connect(
            self.on_next_plot_clicked)

        # Remove when Connector is implemented
        # Previous plot button
        self.plot_navigation_view.previous_plot_button.clicked.connect(
            self.on_previous_plot_clicked)

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
