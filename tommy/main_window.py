from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon
from PySide6.QtGui import QGuiApplication
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget, QHBoxLayout, QVBoxLayout, QSizePolicy, QLayout, QApplication
)

from tommy.support.constant_variables import (
    text_font)
from tommy.view.graph_view import GraphView
from tommy.view.imported_files_view import file_stats_view
from tommy.view.imported_files_view.file_stats_view import FileStatsView
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
        self.set_initial_window_size()
        self.setWindowIcon(QIcon("../assets/tommy.png"))
        self.setStyleSheet("background-color: white;"
                           "font-size: 15px;"
                           f"font-family: {text_font};"
                           "border: none;")

        # Create the main layout
        self.layout = QHBoxLayout()
        self.left_container = QVBoxLayout()
        self.center_container = QVBoxLayout()
        self.right_container = QVBoxLayout()
        self.layout.addLayout(self.left_container)
        self.layout.addLayout(self.center_container)
        self.layout.addLayout(self.right_container)

        # Set spacing of the layout
        self.layout.setSpacing(0)
        self.left_container.setSpacing(0)
        self.center_container.setSpacing(0)
        self.right_container.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)

        # Set the central widget
        central_widget = QWidget()
        central_widget.setLayout(self.layout)
        self.setCentralWidget(central_widget)

        # Create widgets
        self.stopwords_view = StopwordsView()
        self.model_params_view = ModelParamsView()
        self.model_selection_view = ModelSelectionView()
        self.graph_view = GraphView()
        self.information_view = FileStatsView()
        self.plot_navigation_view = PlotNavigationView()
        self.imported_files_view = ImportedFilesView(self.information_view)
        self.fetched_topics_view = FetchedTopicsView(self.information_view)

        # TODO: Remove when Connector is implemented
        self.topic_modelling_handler = TopicModellingHandler(
            self.model_selection_view, self.graph_view,
            self.fetched_topics_view)

        # Initialize widgets
        self.left_container.addWidget(self.model_params_view)
        self.left_container.addWidget(self.stopwords_view)
        self.center_container.addWidget(self.model_selection_view)
        self.center_container.addWidget(self.graph_view)
        self.center_container.addWidget(self.plot_navigation_view)
        self.center_container.addWidget(self.imported_files_view)
        self.right_container.addWidget(self.fetched_topics_view)
        self.right_container.addWidget(
            self.information_view)

        # Make graph view resize with screen
        self.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Expanding,
                                       QSizePolicy.Policy.Expanding))

        self.display_correct_initial_files()
        self.initialize_event_handlers()

    def set_initial_window_size(self) -> None:
        """
        Set the initial window size based on screen size.

        :return: None
        """
        app = QGuiApplication.instance()
        screen = app.primaryScreen()
        screen_geometry = screen.availableGeometry()
        initial_width = max(screen_geometry.width() / 1.5, 1050)
        initial_height = max(screen_geometry.height() / 1.5, 578)
        self.resize(initial_width, initial_height)

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
            lambda tab_index: self.imported_files_view.information_view.
            display_no_component_selected()
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
                self.stopwords_view.additional_stopwords
            )
        )


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University 
(Department of Information and Computing Sciences)
"""
