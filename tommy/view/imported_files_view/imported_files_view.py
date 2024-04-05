import os
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QVBoxLayout, QScrollArea, QWidget

from tommy.controller.corpus_controller import CorpusController
from tommy.controller.project_settings_controller import (
    ProjectSettingsController)

from tommy.view.imported_files_view.file_label import FileLabel
from tommy.view.imported_files_view.file_stats_view import FileStatsView
from tommy.view.observer.observer import Observer
from tommy.support.constant_variables import (
    heading_font, prim_col_red,
    hover_prim_col_red)
from tommy.view.imported_files_view.folder_select_button import (
    FolderSelectButton)


class ImportedFilesView(QWidget, Observer):
    """The ImportedFileDisplay class that shows the imported files."""

    def __init__(self, corpus_controller: CorpusController,
                 project_settings_controller: ProjectSettingsController) -> \
            None:
        """Initialize the ImportedFileDisplay"""
        super().__init__()

        # Set reference to the corpus controller
        self._corpus_controller = corpus_controller
        corpus_controller.add(self)

        # Initialize widget properties
        self.setMinimumHeight(200)
        self.setMaximumHeight(300)
        self.setStyleSheet("background-color: rgba(230, 230, 230, 230);")

        # Initialize layout for the entire widget
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.layout.setSpacing(0)

        # Initialize title label
        self.title_label = None
        self.initialize_title_label()

        # Initialize scroll area and its layout
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_widget)
        self.scroll_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.scroll_area.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scroll_area.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll_area.setWidget(self.scroll_widget)
        self.layout.addWidget(self.scroll_area)

        # Initialize widgets
        self.file_stats_view = FileStatsView()
        self.folder_select_button = FolderSelectButton(
            project_settings_controller)

        self.layout.addWidget(self.folder_select_button)
        # { tab_name, files }
        self.file_container = {}
        self.selected_label = None
        self.selected_file = None

        # Add scroll options
        self.scroll_area.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scroll_area.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll_area.setWidgetResizable(True)

    def initialize_title_label(self) -> None:
        """
        Initialize the title label.

        :return: None
        """
        self.title_label = QLabel("Geïmporteerde bestanden")
        self.title_label.setStyleSheet(f"font-size: 13px;"
                                       f"font-family: {heading_font};"
                                       f"font-weight: bold;"
                                       f"text-transform: uppercase;"
                                       f"background-color: {prim_col_red};"
                                       f"color: white;"
                                       f"border-bottom: "
                                       f"3px solid {hover_prim_col_red};")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter |
                                      Qt.AlignmentFlag.AlignTop)
        self.title_label.setContentsMargins(0, 0, 0, 0)
        self.title_label.setFixedHeight(50)
        self.layout.addWidget(self.title_label)

    def fetch_files(self, tab_name: str) -> None:
        """
        Fetch the metadata from the selected directory and store it in
        file_container
        :return: None
        """
        self.file_container[tab_name] = self._corpus_controller.get_metadata()

    def display_files(self, tab_name: str) -> None:
        """
        Display the files in the layout
        :return: None
        """

        # Clear the layout except for the title label
        # Start from 1 to keep the title label
        for i in reversed(range(0, self.scroll_layout.count())):
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
        if (self.selected_label is not None
                and self.selected_label is not clicked_label):
            self.selected_label.deselect()

        # Set the selected file
        self.selected_file = clicked_label.file

        # Set the selected label
        self.selected_label = clicked_label

        # Display the file stats
        self.file_stats_view.display_file_info(clicked_label.file)

    def initialize_files_for_label(self, tab_name: str, files: list) -> None:
        """
        Initialize the files for the given label
        :param tab_name: The name of the tab
        :param files: The list of files
        :return: None
        """
        self.file_container[tab_name] = files

    def update_observer(self, publisher) -> None:
        """
        Update the observer. This fetches and displays the files when the
        metadata is updated.
        :param publisher: The publisher that is being observed
        :return: None
        """
        # TODO: when the implementation of tabs is updated, it should no longer
        #  hard-code the tab name
        self.fetch_files("lda_model")
        self.display_files("lda_model")
        print("fetched and displayed files")


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University 
(Department of Information and Computing Sciences)
"""
