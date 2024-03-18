from PySide6.QtCore import QSize
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget
)

from tommy.support.constant_variables import (
    text_font)
from tommy.view.graph_view import GraphView
from tommy.view.imported_files_view. \
    imported_files_view import ImportedFilesView
from tommy.view.model_params_view import (
    ModelParamsView)
from tommy.view.model_selection_view import (
    ModelSelectionView)
from tommy.view.plot_navigation_view import (
    PlotNavigationView)
from tommy.view.stopwords_view import (
    StopwordsView)
from tommy.view.topic_modelling_handler import \
    TopicModellingHandler
from tommy.view.topic_view.fetched_topics_view import \
    FetchedTopicsView


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
        self.fetched_topics_view = FetchedTopicsView()

        # TODO: Remove when Connector is implemented
        self.topic_modelling_handler = TopicModellingHandler(
            self.model_selection_view, self.graph_view,
            self.fetched_topics_view)

        # Initialize widgets
        self.initialize_widget(self.model_params_view,
                               0, 0, 250, 300)
        self.initialize_widget(self.imported_files_view.stopwords_display,
                               0, 300, 250, 397)
        self.initialize_widget(self.imported_files_view,
                               250, 458, 700, 240)
        self.initialize_widget(self.imported_files_view.file_stats_display,
                               950, 458, 250, 240)
        self.initialize_widget(self.fetched_topics_view,
                               950, 0, 250, 458)
        self.initialize_widget(self.graph_view,
                               250, 50, 700, 360)
        self.initialize_widget(self.plot_navigation_view,
                               250, 408, 700, 50)
        # TODO: Uncomment when Connector is implemented
        self.initialize_widget(self.model_selection_view,
                               250, 0, 700, 50)
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
        # Get plot to display
        active_tab_name = self.model_selection_view.get_active_tab_name()

        # Get the next plot index
        self.topic_modelling_handler.plot_index[active_tab_name] += 1
        self.topic_modelling_handler.plot_index[active_tab_name] %= len(
            self.topic_modelling_handler.plots_container[active_tab_name])

        # Get the canvas from the plots container
        canvas = self.topic_modelling_handler.plots_container[active_tab_name][
            self.topic_modelling_handler.plot_index[active_tab_name]]

        # Display the plot
        self.graph_view.display_plot(canvas)

    # TODO: Extract method when Connector is implemented
    def on_previous_plot_clicked(self) -> None:
        """
        Event handler for when the previous plot button is clicked.

        :return: None
        """
        # Get plot to display
        active_tab_name = self.model_selection_view.get_active_tab_name()

        # Get the previous plot index
        self.topic_modelling_handler.plot_index[active_tab_name] -= 1
        self.topic_modelling_handler.plot_index[active_tab_name] %= len(
            self.topic_modelling_handler.plots_container[active_tab_name])

        # Get the canvas from the plots container
        canvas = self.topic_modelling_handler.plots_container[active_tab_name][
            self.topic_modelling_handler.plot_index[active_tab_name]]

        # Display the plot
        self.graph_view.display_plot(canvas)

    # TODO: Extract method when Connector is implemented
    def display_correct_initial_files(self) -> None:
        """
        Display the correct initial files in the main window.

        :return: None
        """
        self.imported_files_view.fetch_files(
            self.model_selection_view.get_active_tab_name())
        self.imported_files_view.display_files(
            self.model_selection_view.get_active_tab_name())

    # TODO: Extract method when Connector is implemented
    # Some of the event handlers can be used to update observers
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
        self.model_selection_view.tabBarClicked.connect(
            lambda tab_index: self.imported_files_view.display_files(
                self.model_selection_view.tabText(tab_index))
        )

        # Connecting the tabBarClicked signal to a method in
        # ImportedFilesDisplay
        self.model_selection_view.tabBarClicked.connect(
            lambda tab_index: self.imported_files_view.file_stats_display.
            display_no_file_selected()
        )

        # Connecting the tabBarClicked signal to a method in
        # FetchedTopicsView
        self.model_selection_view.tabBarClicked.connect(
            lambda tab_index: self.fetched_topics_view.display_topics(
                self.model_selection_view.tabText(tab_index))
        )

        # Connecting the tabBarClicked signal to a method in GraphView
        self.model_selection_view.tabBarClicked.connect(
            lambda tab_index: self.graph_view.display_plot(
                self.topic_modelling_handler.plots_container[
                    self.model_selection_view.tabText(tab_index)][0])
        )

        # Connecting the apply button to the graph view
        self.model_params_view.apply_button.clicked.connect(
            lambda: self.topic_modelling_handler.apply_topic_modelling(
                self.imported_files_view.file_container[
                    self.model_selection_view.get_active_tab_name()],
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
