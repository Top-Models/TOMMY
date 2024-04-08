from PySide6.QtGui import QIcon, QGuiApplication
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget, QHBoxLayout, QVBoxLayout, QSizePolicy
)

from tommy.controller.controller import Controller
from tommy.support.constant_variables import (
    text_font)
from tommy.view.graph_view import GraphView
from tommy.view.imported_files_view.imported_files_view import (
    ImportedFilesView)
from tommy.view.menu_bar import MenuBar
from tommy.view.model_params_view import (
    ModelParamsView)
from tommy.view.model_selection_view import (
    ModelSelectionView)
from tommy.view.plot_navigation_view import (
    PlotNavigationView)
from tommy.view.stopwords_view import (
    StopwordsView)
from tommy.view.topic_view.fetched_topics_view import \
    FetchedTopicsView


class MainWindow(QMainWindow):
    """Main window class for the topic modelling application"""

    def __init__(self) -> None:
        """Initialize the main window."""
        super().__init__()

        # Create the main Controller
        self._controller: Controller = Controller()

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

        # Initialize the menu bar
        self.setMenuBar(MenuBar(self,
                                self._controller.project_settings_controller))

        # Create widgets
        self.stopwords_view = StopwordsView(
            self._controller.stopwords_controller)
        self.model_selection_view = ModelSelectionView()
        self.imported_files_view = ImportedFilesView(
            self._controller.corpus_controller,
            self._controller.project_settings_controller)
        self.model_params_view = ModelParamsView(
            self._controller.model_parameters_controller,
            self._controller)
        self.graph_view = GraphView(self._controller.graph_controller)
        self.plot_navigation_view = PlotNavigationView(
            self._controller.graph_controller)
        self.fetched_topics_view = FetchedTopicsView(
            self._controller.graph_controller)

        # Initialize widgets
        self.left_container.addWidget(self.model_params_view)
        self.left_container.addWidget(self.stopwords_view)
        self.center_container.addWidget(self.model_selection_view)
        self.center_container.addWidget(self.graph_view)
        self.center_container.addWidget(self.plot_navigation_view)
        self.center_container.addWidget(self.imported_files_view)
        self.right_container.addWidget(self.fetched_topics_view)
        self.right_container.addWidget(
            self.imported_files_view.file_stats_view)

        # Make graph view resize with screen
        self.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Expanding,
                                       QSizePolicy.Policy.Expanding))

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
    def display_correct_initial_files(self) -> None:
        """
        Display the correct initial files in the main window.
        Setting the input folder path in the project settings will
        automatically notify the corpus model to extract the metadata from
        the files. Once the metadata is extracted, the imported files view
        will automatically get updated.
        :return: None
        """

        # TODO: the default input folder path is currently hardcoded in
        #  project_settings_model, rethink whether it should be hardcoded or
        #  be loaded from a project instead
        # get and immediately reset the input folder path to cause the
        # project settings controller to notify its observers
        path = (self._controller.project_settings_controller
                .get_input_folder_path())
        self._controller.project_settings_controller.set_input_folder_path(
            path)

    # TODO: Extract method when Connector is implemented
    # Some of the event handlers can be used to update observers
    def initialize_event_handlers(self) -> None:
        """
        Initialize event handlers for the main window.

        :return: None
        """

        # Connecting the tabBarClicked signal to a method in
        # ImportedFilesDisplay
        self.model_selection_view.tabBarClicked.connect(
            lambda tab_index: self.imported_files_view.display_files(
                self.model_selection_view.tabText(tab_index))
        )

        # Connecting the tabBarClicked signal to a method in
        # ImportedFilesDisplay
        self.model_selection_view.tabBarClicked.connect(
            lambda tab_index: self.imported_files_view.file_stats_view.
            display_no_file_selected()
        )


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University 
(Department of Information and Computing Sciences)
"""
