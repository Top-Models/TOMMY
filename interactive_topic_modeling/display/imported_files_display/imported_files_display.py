from PySide6.QtCore import Qt
from PySide6.QtWidgets import QVBoxLayout, QScrollArea, QWidget

from interactive_topic_modeling.backend.file_import.file_reader import FileReader
from interactive_topic_modeling.display.imported_files_display.file_label import FileLabel
from interactive_topic_modeling.display.imported_files_display.file_stats_display import FileStatsDisplay
from interactive_topic_modeling.display.stopwords_display import StopwordsDisplay
from interactive_topic_modeling.support import project_settings
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

        # Initialize file list
        # TODO: Convert to list of File objects later (with needed properties)
        self.files = ["file1.csv", "file2.csv", "file3.csv", "file4.csv", "file5.csv", "file6.csv"]
        self.selected_label = None

        # Add scroll options
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setWidgetResizable(True)

        # Add widgets
        self.display_files()

    def fetch_files(self) -> None:
        """
        Fetch the files from the selected directory
        :return: The list of files
        """
        all_files = list(self.file_reader.read_files(current_project_settings.selected_folder))
        self.files = [file.split("/")[-1] for file in all_files]

    def display_files(self) -> None:
        """
        Display the files in the layout
        :return: None
        """

        self.fetch_files()

        # Clear the layout
        for i in reversed(range(self.layout.count())):
            self.layout.itemAt(i).widget().deleteLater()

        # Add the file labels to the layout
        for file in self.files:
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
