import os
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QLabel, QVBoxLayout, QScrollArea, QWidget,
                               QSizePolicy, QPushButton, QGridLayout)

from tommy.backend.file_import.file import File
from tommy.backend.file_import.file_reader import FileReader
from tommy.view.imported_files_view.file_label import FileLabel
from tommy.view.imported_files_view.file_stats_view import FileStatsView
from tommy.view.observer.observer import Observer
from tommy.view.stopwords_view import StopwordsView
from tommy.support.constant_variables import (heading_font, prim_col_red,
                                              hover_prim_col_red)
from tommy.support.project_settings import current_project_settings


class ImportedFilesView(QWidget, Observer):
    """The ImportedFileDisplay class that shows the imported files."""

    def __init__(self) -> None:
        """Initialize the ImportedFileDisplay"""
        super().__init__()

        # Initialize file reader
        self.file_reader = FileReader()

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
        self.title_widget = None
        self.initialize_title_widget()

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

        self.scroll_area.setVisible(True)
        self.setSizePolicy(QSizePolicy.Policy.Expanding,
                           QSizePolicy.Policy.Expanding)

        # Initialize widgets
        self.file_stats_view = FileStatsView()

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

    def initialize_title_widget(self) -> None:
        """
        Initialize the title label.
        :return: None
        """

        # Make a widget to add the title label and collapse button
        self.title_widget = QWidget()
        self.title_widget.setFixedHeight(50)

        # Initialize layout for the title widget
        title_layout = QGridLayout(self.title_widget)
        title_layout.setContentsMargins(0, 0, 0, 0)
        title_layout.setSpacing(0)

        # Create the title label
        self.title_widget.title_label = QLabel("Geïmporteerde bestanden")
        (self.title_widget.title_label.
         setStyleSheet(f"font-size: 13px;"
                       f"font-family: {heading_font};"
                       f"font-weight: bold;"
                       f"text-transform: uppercase;"
                       f"background-color: {prim_col_red};"
                       f"color: white;"
                       f"border-bottom: "
                       f"3px solid {hover_prim_col_red};"))

        # Align the title label to the center
        self.title_widget.title_label.setAlignment(
                Qt.AlignmentFlag.AlignCenter)
        self.title_widget.title_label.setContentsMargins(50, 0, 0, 0)

        # Create the title button
        self.title_widget.title_button = QPushButton("🡻")
        (self.title_widget.title_button.
         setStyleSheet(f"font-size: 13px;"
                       f"font-family: {heading_font};"
                       f"font-weight: bold;"
                       f"text-transform: uppercase;"
                       f"background-color: {prim_col_red};"
                       f"color: white;"
                       f"border-bottom: "
                       f"3px solid {hover_prim_col_red};"
                       "}"
                       "QPushButton:hover {"
                       f"background-color: {hover_prim_col_red};"))
        self.title_widget.title_button.setFixedSize(50, 50)

        # Add the title label and button to the layout
        title_layout.addWidget(self.title_widget.title_label, 0, 1)
        title_layout.addWidget(self.title_widget.title_button, 0, 2)
        self.layout.addWidget(self.title_widget)

        # Connect label click event to toggle_collapse method
        self.title_widget.title_button.mousePressEvent = self.toggle_collapse

    def fetch_files(self, tab_name: str) -> None:
        """
        Fetch the files from the selected directory
        :return: The list of files
        """
        all_files = list(self.file_reader.read_files(
                current_project_settings.selected_folder))
        self.file_container[tab_name] = all_files

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

    def toggle_collapse(self, clicked_header) -> None:
        """
        Toggle visibility of the scroll area and adjust layout accordingly.
        """
        self.collapse_component()
        self.change_header_appearance()

    def change_header_appearance(self) -> None:
        """
        Change the appearance of the header.
        """

        if self.scroll_area.isVisible():
            self.title_widget.title_button.setText("🡻")
        else:
            self.title_widget.title_button.setText("🡹")

    def collapse_component(self) -> None:
        """
        Collapse the imported files display.
        """
        if self.scroll_area.isVisible():
            # Hide the scroll area
            self.scroll_area.setVisible(False)
            # Move the header to the bottom of the layout
            self.layout.addStretch(0.1)
            self.layout.addWidget(self.title_widget)
            # Fix widget size to allow entire layout to be moved to
            self.setFixedHeight(self.title_widget.height())
        else:
            # Show the scroll area
            self.scroll_area.setVisible(True)
            # Remove the stretch from the layout to move the header
            # back to its original position
            self.layout.removeWidget(self.title_widget)
            self.layout.insertWidget(0, self.title_widget)
            self.layout.removeItem(self.layout.itemAt(self.layout.count() - 1))
            # Restore actual height
            self.setMinimumHeight(200)
            self.setMaximumHeight(300)

    def update_observer(self, publisher) -> None:
        """
        Update the observer.
        :param publisher: The publisher that is being observed
        :return: None
        """
        pass


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University 
(Department of Information and Computing Sciences)
"""
