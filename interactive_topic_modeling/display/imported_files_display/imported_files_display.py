from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QVBoxLayout, QScrollArea, QWidget

from interactive_topic_modeling.backend.file_import.file import File
from interactive_topic_modeling.backend.file_import.file_reader import FileReader
from interactive_topic_modeling.display.imported_files_display.file_label import FileLabel
from interactive_topic_modeling.display.imported_files_display.file_stats_display import FileStatsDisplay
from interactive_topic_modeling.display.stopwords_display import StopwordsDisplay
from interactive_topic_modeling.support.constant_variables import heading_font, seco_col_blue, hover_seco_col_blue
from interactive_topic_modeling.support.project_settings import current_project_settings


class ImportedFilesDisplay(QWidget):

    def __init__(self):
        super().__init__()

        # Initialize file reader
        self.file_reader = FileReader()

        # Initialize widget properties
        self.setStyleSheet("background-color: rgba(230, 230, 230, 230);")

        # Initialize layout for the entire widget
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Initialize title label
        self.title_label = QLabel("Geïmporteerde bestanden")
        self.title_label.setStyleSheet(f"font-size: 13px;"
                                       f"font-family: {heading_font};"
                                       f"font-weight: bold;"
                                       f"text-transform: uppercase;"
                                       f"background-color: {seco_col_blue};"
                                       f"color: white;"
                                       f"border-bottom: 3px solid {hover_seco_col_blue};")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)
        self.title_label.setContentsMargins(0, 0, 0, 0)
        self.title_label.setMinimumHeight(50)
        self.layout.addWidget(self.title_label)

        # Initialize scroll area and its layout
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_widget)
        self.scroll_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll_area.setWidget(self.scroll_widget)
        self.layout.addWidget(self.scroll_area)

        # Initialize widgets
        self.stopwords_display = StopwordsDisplay()
        self.file_stats_display = FileStatsDisplay()

        # { tab_name, files }
        self.file_container = {}
        self.selected_label = None
        self.selected_file = None

        # Add scroll options
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll_area.setWidgetResizable(True)

    def fetch_files(self, tab_name: str) -> None:
        """
        Fetch the files from the selected directory
        :return: The list of files
        """
        all_files = list(self.file_reader.read_files(current_project_settings.selected_folder))
        files_to_add = [File(file.split("/")[-1]) for file in all_files]
        self.file_container[tab_name] = files_to_add

    def display_files(self, tab_name: str) -> None:
        """
        Display the files in the layout
        :return: None
        """

        # Clear the layout except for the title label
        for i in reversed(range(0, self.scroll_layout.count())):  # Start from 1 to keep the title label
            self.scroll_layout.itemAt(i).widget().deleteLater()

        # Check if the tab name is in the file container
        if tab_name not in self.file_container:
            return

        # Add the file labels to the layout
        for file in self.file_container[tab_name]:
            file_label = FileLabel(file, self.scroll_area)
            file_label.clicked.connect(self.label_clicked)
            self.scroll_layout.addWidget(file_label)

    def label_clicked(self, clicked_label) -> None:
        """
        Handle the click event on a file label
        :param clicked_label: The label that was clicked
        :return: None
        """

        # Deselect the previously selected label
        if self.selected_label is not None and self.selected_label is not clicked_label:
            self.selected_label.deselect()

        # Set the selected file
        self.selected_file = clicked_label.file

        # Set the selected label
        self.selected_label = clicked_label

        # Display the file stats
        self.file_stats_display.display_file_info(clicked_label.file)

    def initialize_files_for_label(self, tab_name: str, files: list) -> None:
        """
        Initialize the files for the given label
        :param tab_name: The name of the tab
        :param files: The list of files
        :return: None
        """
        self.file_container[tab_name] = files
