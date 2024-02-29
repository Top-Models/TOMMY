from PySide6.QtCore import Qt
from PySide6.QtWidgets import QVBoxLayout, QScrollArea, QWidget

from interactive_topic_modeling.backend.file_import.file import File
from interactive_topic_modeling.backend.file_import.file_reader import FileReader
from interactive_topic_modeling.display.imported_files_display.file_label import FileLabel
from interactive_topic_modeling.display.imported_files_display.file_stats_display import FileStatsDisplay
from interactive_topic_modeling.display.stopwords_display import StopwordsDisplay
from interactive_topic_modeling.support.project_settings import current_project_settings


class ImportedFilesDisplay(QScrollArea):
    def __init__(self):
        super().__init__()

        # Initialize file reader
        self.file_reader = FileReader()

        # Initialize widget properties
        self.setStyleSheet("background-color: white;")

        # Initialize layout for scroll area
        self.scroll_area = QWidget()
        self.layout = QVBoxLayout(self.scroll_area)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.setWidget(self.scroll_area)

        # Initialize widgets
        self.stopwords_display = StopwordsDisplay()
        self.file_stats_display = FileStatsDisplay()

        # { tab_name, files }
        self.file_container = {}
        self.selected_label = None

        # Add scroll options
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setWidgetResizable(True)

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

        # Clear the layout
        for i in reversed(range(self.layout.count())):
            self.layout.itemAt(i).widget().deleteLater()

        # Check if the tab name is in the file container
        if tab_name not in self.file_container:
            return

        # Add the file labels to the layout
        for file in self.file_container[tab_name]:
            file_label = FileLabel(file, self.scroll_area)
            file_label.clicked.connect(self.label_clicked)
            self.layout.addWidget(file_label)

    def label_clicked(self, clicked_label) -> None:
        """
        Handle the click event on a file label
        :param clicked_label: The label that was clicked
        :return: None
        """

        # Deselect the previously selected label
        if self.selected_label is not None and self.selected_label is not clicked_label:
            self.selected_label.deselect()

        # Set the selected label
        self.selected_label = clicked_label

    def initialize_files_for_label(self, tab_name: str, files: list) -> None:
        """
        Initialize the files for the given label
        :param tab_name: The name of the tab
        :param files: The list of files
        :return: None
        """
        self.file_container[tab_name] = files
