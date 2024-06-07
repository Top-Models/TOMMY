from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QGuiApplication, QPainter, QColor
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget, QHBoxLayout, QVBoxLayout, QSizePolicy, QSplitter, QSplitterHandle
)

from tommy.controller.controller import Controller
from tommy.support.constant_variables import (
    text_font)
from tommy.view.graph_view import GraphView
from tommy.view.imported_files_view.file_label import FileLabel
from tommy.view.imported_files_view.imported_files_view import (
    ImportedFilesView)
from tommy.view.menu_bar import MenuBar
from tommy.view.settings_view.model_params_view import (
    ModelParamsView)
from tommy.view.plot_selection_view import (
    PlotSelectionView)
from tommy.view.selected_information_view import SelectedInformationView
from tommy.view.stopwords_view import (
    StopwordsView)
from tommy.view.supporting_components.custom_splitter.custom_splitter_component import \
    CustomSplitter
from tommy.view.topic_view.fetched_topics_view import \
    FetchedTopicsView
from tommy.view.topic_view.topic_entity_component.topic_entity import (
    TopicEntity)


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
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        # Create the custom splitter to handle resizing
        self.splitter = CustomSplitter(Qt.Horizontal)
        self.splitter.setStyleSheet("border: none;")
        self.splitter.setContentsMargins(0, 0, 0, 0)

        self.left_container = QWidget()
        self.left_layout = QVBoxLayout(self.left_container)
        self.left_layout.setContentsMargins(0, 0, 0, 0)
        self.left_layout.setSpacing(0)

        self.center_container = QWidget()
        self.center_layout = QVBoxLayout(self.center_container)
        self.center_layout.setContentsMargins(0, 0, 0, 0)
        self.center_layout.setSpacing(0)

        self.right_container = QWidget()
        self.right_layout = QVBoxLayout(self.right_container)
        self.right_layout.setContentsMargins(0, 0, 0, 0)
        self.right_layout.setSpacing(0)

        self.splitter.addWidget(self.left_container)
        self.splitter.addWidget(self.center_container)
        self.splitter.addWidget(self.right_container)

        # Adjust size policies and minimum widths
        self.left_container.setSizePolicy(QSizePolicy.Fixed,
                                          QSizePolicy.Expanding)
        self.right_container.setSizePolicy(QSizePolicy.Expanding,
                                           QSizePolicy.Expanding)
        self.center_container.setSizePolicy(QSizePolicy.Expanding,
                                            QSizePolicy.Expanding)

        self.layout.addWidget(self.splitter)

        # Set the central widget
        central_widget = QWidget()
        central_widget.setLayout(self.layout)
        self.setCentralWidget(central_widget)

        # Initialize the menu bar
        self.setMenuBar(MenuBar(self,
                                self._controller.project_settings_controller,
                                self._controller.saving_loading_controller,
                                self._controller.export_controller))

        # Create widgets
        self.stopwords_view = StopwordsView(
            self._controller.stopwords_controller)
        self.graph_view = GraphView()
        self.plot_selection_view = PlotSelectionView(
            self._controller.graph_controller,
            self._controller.config_controller,
            self.graph_view
        )
        self.imported_files_view = ImportedFilesView(
            self._controller.corpus_controller,
            self._controller.topic_modelling_controller)
        self.model_params_view = ModelParamsView(
            self._controller.model_parameters_controller,
            self._controller.language_controller,
            self._controller.config_controller,
            self._controller.topic_modelling_controller)
        self.fetched_topics_view = FetchedTopicsView(
            self._controller.graph_controller,
            self._controller.model_parameters_controller)
        self.selected_information_view = SelectedInformationView(
            self._controller.graph_controller,
            self._controller.model_parameters_controller)

        # Initialize widgets
        self.left_layout.addWidget(self.model_params_view)
        self.left_layout.addWidget(self.stopwords_view)
        self.center_layout.addWidget(self.plot_selection_view)
        self.center_layout.addWidget(self.graph_view)
        self.center_layout.addWidget(self.imported_files_view)
        self.right_layout.addWidget(self.fetched_topics_view)
        self.right_layout.addWidget(self.selected_information_view)

        # Adjust the splitter stretch factors
        self.splitter.setStretchFactor(0, 1)
        self.splitter.setStretchFactor(1, 3)
        self.splitter.setStretchFactor(2,
                                       1)

        self.display_correct_initial_files()

        # Initialize event handlers
        self.imported_files_view.fileClicked.connect(self.on_file_clicked)
        self.fetched_topics_view.topicClicked.connect(self.on_topic_clicked)
        self.fetched_topics_view.topicNameChanged.connect(
            self.on_topic_name_changed)

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

    def on_file_clicked(self, file: FileLabel) -> None:
        """
        Event handler for when a file is clicked.

        :param file: The file that was clicked
        :return: None
        """
        self.fetched_topics_view.deselect_all_topics()
        self.fetched_topics_view.selected_topic = None

        # TODO: Hardcoded save name
        # Show info about run if no file is selected
        if not file.selected:
            self.selected_information_view.display_run_info("lda_model")
            return

        self.selected_information_view.display_file_info(file)

    def on_topic_clicked(self, topic_entity: TopicEntity) -> None:
        """
        Event handler for when a topic is clicked.

        :param topic_entity: The topic that was clicked
        :return: None
        """
        self.imported_files_view.deselect_all_files()
        self.imported_files_view.selected_label = None

        # TODO: Hardcoded save name
        # Show info about run if no topic is selected
        if not topic_entity.selected:
            self.imported_files_view.display_files()
            self.selected_information_view.display_run_info("lda_model")
            return

        self.imported_files_view.on_topic_selected(topic_entity)
        self.selected_information_view.display_topic_info(topic_entity)

    def on_topic_name_changed(self, topic_entity: TopicEntity) -> None:
        """
        Event handler for when a topic name is changed.

        :param topic_entity: The topic entity whose name was changed
        :return: None
        """
        if topic_entity.selected:
            self.selected_information_view.display_topic_info(topic_entity)

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

    @property
    def controller(self):
        return self._controller


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University
(Department of Information and Computing Sciences)
"""
