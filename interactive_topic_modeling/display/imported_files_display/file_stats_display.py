from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QScrollArea, QVBoxLayout, QLayout

from interactive_topic_modeling.backend.file_import.file import File
from interactive_topic_modeling.support.constant_variables import (
    seco_col_blue,
    heading_font,
    hover_seco_col_blue)


class FileStatsDisplay(QScrollArea):
    """Class to define the FileStatsDisplay UI component"""

    def __init__(self) -> None:
        """Initialize the FileStatsDisplay."""
        super().__init__()

        # Initialize widget properties
        self.setStyleSheet(f"background-color: white;"
                           f"color: black;")
        self.setMinimumHeight(200)

        # Initialize layout
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Add title widget
        self.add_title_widget()

        # Initialize widgets
        self.display_no_file_selected()

    def add_title_widget(self) -> None:
        """
        Add the title label widget
        """
        title_label = QLabel("Bestandsinformatie")
        title_label.setStyleSheet(f"font-size: 13px;"
                                  f"font-family: {heading_font};"
                                  f"font-weight: bold;"
                                  f"text-transform: uppercase;"
                                  f"background-color: {seco_col_blue};"
                                  f"color: white;"
                                  f"border-bottom: "
                                  f"3px solid {hover_seco_col_blue};")

        title_label.setContentsMargins(0, 0, 0, 0)
        title_label.setMaximumHeight(50)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter |
                                 Qt.AlignmentFlag.AlignTop)
        self.layout.addWidget(title_label)

    def display_no_file_selected(self) -> None:
        """
        Display a message when no file is selected.
        :return: None
        """
        # Prepare layout
        self.clear_layout()
        self.layout.setContentsMargins(0, 0, 0, 0)

        # Add label
        no_file_selected_label = QLabel("Geen bestand geselecteerd")
        no_file_selected_label.setStyleSheet("font-size: 20px;")
        no_file_selected_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(no_file_selected_label)

    def clear_layout(self) -> None:
        """
        Clear the layout.
        :return: None
        """
        while self.layout.count() > 1:
            item = self.layout.takeAt(1)
            if item:
                layout = item.layout()
                if layout:
                    self.clear_sub_layout(layout)
            widget = item.widget()
            if widget:
                widget.deleteLater()

    def clear_sub_layout(self, layout: QLayout) -> None:
        """
        Clear a sub-layout
        :param layout: The sub-layout to clear
        :return: None
        """
        while layout.count() > 0:
            item = layout.takeAt(0)
            if item:
                widget = item.widget()
                if widget:
                    widget.deleteLater()
                else:
                    self.clear_sub_layout(item.layout())

    def display_file_info(self, file: File) -> None:
        """
        Display the file info
        :param file: The file to display
        :return: None
        """

        # Prepare layout
        self.clear_layout()

        # Use a vertical layout
        vertical_layout = QVBoxLayout()
        vertical_layout.setAlignment(Qt.AlignmentFlag.AlignTop |
                                     Qt.AlignmentFlag.AlignLeft)

        # Adjust the left margin here
        vertical_layout.setContentsMargins(20, 20, 0, 0)
        vertical_layout.setSpacing(10)
        self.layout.addLayout(vertical_layout)

        # Add file name
        file_name_label = QLabel(f"{file.name}")
        file_name_label.setStyleSheet("font-size: 20px;"
                                      f"font-family: {heading_font};"
                                      f"font-weight: bold;"
                                      f"text-transform: uppercase;")
        file_name_label.setAlignment(Qt.AlignmentFlag.AlignLeft |
                                     Qt.AlignmentFlag.AlignTop)
        vertical_layout.addWidget(file_name_label)

        # Add file path
        file_path_label = QLabel(f"Pad: {file.path}")
        file_path_label.setStyleSheet("font-size: 16px;")
        file_path_label.setAlignment(Qt.AlignmentFlag.AlignLeft |
                                     Qt.AlignmentFlag.AlignTop)
        vertical_layout.addWidget(file_path_label)

        # Add file format
        file_format_label = QLabel(f"Formaat: {file.format}")
        file_format_label.setStyleSheet("font-size: 16px;")
        file_format_label.setAlignment(Qt.AlignmentFlag.AlignLeft |
                                       Qt.AlignmentFlag.AlignTop)
        vertical_layout.addWidget(file_format_label)

        # Add word amount
        word_amount_label = QLabel(f"Aantal woorden: {file.length}")
        word_amount_label.setStyleSheet("font-size: 16px;")
        word_amount_label.setAlignment(Qt.AlignmentFlag.AlignLeft |
                                       Qt.AlignmentFlag.AlignTop)
        vertical_layout.addWidget(word_amount_label)

        # Add file size
        file_size_label = QLabel(f"Grootte: {file.size}B")
        file_size_label.setStyleSheet("font-size: 16px;")
        file_size_label.setAlignment(Qt.AlignmentFlag.AlignLeft |
                                     Qt.AlignmentFlag.AlignTop)
        vertical_layout.addWidget(file_size_label)
