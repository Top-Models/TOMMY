from PySide6.QtCore import Qt
from PySide6.QtCore import Signal
from PySide6.QtWidgets import (QLabel, QVBoxLayout, QScrollArea, QWidget,
                               QSizePolicy, QPushButton, QGridLayout)

from tommy.controller.corpus_controller import CorpusController
from tommy.controller.file_import.metadata import Metadata
from tommy.controller.file_import.processed_corpus import ProcessedCorpus
from tommy.controller.file_import.processed_file import ProcessedFile
from tommy.controller.topic_modelling_controller import TopicModellingController
from tommy.support.constant_variables import (
    heading_font, prim_col_red,
    hover_prim_col_red, scrollbar_style)
from tommy.support.types import Document_topics

from tommy.view.imported_files_view.file_label import FileLabel
from tommy.view.topic_view.topic_entity_component.topic_entity import \
    TopicEntity


class ImportedFilesView(QWidget):
    """The ImportedFileDisplay class that shows the imported files."""

    fileClicked = Signal(object)

    def __init__(self, corpus_controller: CorpusController,
                 topic_modelling_controller: TopicModellingController) -> None:
        """Initialize the ImportedFileDisplay"""
        super().__init__()

        # Set reference to the corpus controller and subscribe to the metadata
        self._corpus_controller = corpus_controller
        corpus_controller.metadata_changed_event.subscribe(
            self.on_metadata_changed)

        topic_modelling_controller.model_trained_event.subscribe(
            lambda _: self.display_files())

        topic_modelling_controller.calculate_topic_documents_event.subscribe(
            self.on_document_topics_calculated)

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
        self.scroll_area.setWidget(self.scroll_widget)
        self.scroll_area.setStyleSheet(scrollbar_style)
        self.layout.addWidget(self.scroll_area)

        self.scroll_area.setVisible(True)
        self.setSizePolicy(QSizePolicy.Policy.Expanding,
                           QSizePolicy.Policy.Expanding)

        self.metadata: list[Metadata] = []
        self.document_topics: Document_topics = []
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
        self.title_widget.title_button = QPushButton("▽")
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

    def display_files(self) -> None:
        """
        Display the metadata from files in the layout
        :return: None
        """

        # Clear the layout except for the title label
        # Start from 1 to keep the title label
        for i in reversed(range(0, self.scroll_layout.count())):
            self.scroll_layout.itemAt(i).widget().deleteLater()

        sorted_files = sorted(self.metadata, key=lambda x: x.name)

        # Add the file labels to the layout
        for file in sorted_files:
            file_label = FileLabel(file, self.scroll_area)
            file_label.clicked.connect(self.label_clicked)
            self.scroll_layout.addWidget(file_label)

    def display_files_for_topic(self, topic: TopicEntity) -> None:
        """
        Display the metadata from files in the layout
        Sorted by topic document correspondence
        :return: None
        """

        index = topic.index

        # Clear the layout except for the title label
        # Start from 1 to keep the title label
        for i in reversed(range(0, self.scroll_layout.count())):
            self.scroll_layout.itemAt(i).widget().deleteLater()

        sorted_files = sorted(self.document_topics, key=lambda x: x[1][index],
                              reverse=True)

        # Add the file labels to the layout
        for (metadata, topic_correspondence) in sorted_files:
            file_label = FileLabel(metadata, self.scroll_area,
                                   topic_correspondence=
                                   topic_correspondence[index])
            file_label.clicked.connect(self.label_clicked)
            self.scroll_layout.addWidget(file_label)

    def deselect_all_files(self) -> None:
        """
        Deselect all the files
        :return: None
        """
        for i in range(self.scroll_layout.count()):
            file_label = self.scroll_layout.itemAt(i).widget()
            file_label.deselect()

    def label_clicked(self, clicked_label: FileLabel) -> None:
        """
        Handle the click event on a file label
        :param clicked_label: The label that was clicked
        :return: None
        """

        # Deselect the previously selected label
        self.deselect_all_files()

        # Select the clicked label
        if self.selected_label == clicked_label:
            self.selected_label = None
            clicked_label.enterEvent(None)
        else:
            self.selected_label = clicked_label
            clicked_label.select()

        # Display the file stats
        self.fileClicked.emit(clicked_label)

    def toggle_collapse(self, clicked_header) -> None:
        """
        Toggle visibility of the scroll area and adjust layout accordingly.
        """
        self.collapse_component()
        self.change_button_appearance()

    def change_button_appearance(self) -> None:
        """
        Change the appearance of the toggle button.
        """
        if self.scroll_area.isVisible():
            self.title_widget.title_button.setText("▽")
        else:
            self.title_widget.title_button.setText("△")

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

            # Restore beginning height
            self.setMinimumHeight(200)
            self.setMaximumHeight(300)

    def on_metadata_changed(self, metadata: list[Metadata]) -> None:
        """
        Update the files tab with the current file metadata.
        :param metadata: The new list of metadata for the current tab
        :return: None
        """

        self.metadata = metadata
        self.display_files()

    def on_document_topics_calculated(
            self,
            document_topics: Document_topics) -> None:
        """
        Update stored topic document correspondence reference.
        :param document_topics: The list of documents related to topics
        :return: None
        """

        self.document_topics = document_topics

    def on_topic_selected(self, topic: TopicEntity) -> None:
        """
        Update the files tab including topic document correspondence.
        :param topic: the current selected topic
        :return: None
        """

        if not self.document_topics:
            print("No document topics correspondence was calculated, skipping"
                  "displaying files for topic.")
            return

        self.display_files_for_topic(topic)


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University
(Department of Information and Computing Sciences)
"""
