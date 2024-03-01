from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QScrollArea, QVBoxLayout

from interactive_topic_modeling.backend.file_import.file import File
from interactive_topic_modeling.support.constant_variables import seco_col_blue, heading_font


class FileStatsDisplay(QScrollArea):

    def __init__(self):
        super().__init__()

        # Initialize widget properties
        self.setStyleSheet(f"background-color: {seco_col_blue};")

        # Initialize layout
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(20, 20, 0, 0)
        self.setLayout(self.layout)

        # Title widget
        title_label = QLabel("File stats")
        title_label.setStyleSheet("font-size: 20px;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

        # Initialize widgets
        self.display_no_file_selected()

    def display_no_file_selected(self) -> None:
        """
        Display a message when no file is selected
        :return: None
        """
        no_file_selected_label = QLabel("No file selected")
        no_file_selected_label.setStyleSheet("font-size: 20px;")
        no_file_selected_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(no_file_selected_label)

    def clear_screen(self):
        """
        Clear the screen
        :return: None
        """
        for i in reversed(range(self.layout.count())):
            self.layout.itemAt(i).widget().deleteLater()

    def display_file_info(self, file: File):
        """
        Display the file info
        :param file: The file to display
        :return: None
        """
        self.clear_screen()

        # Use a vertical layout
        vertical_layout = QVBoxLayout()
        vertical_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.layout.addLayout(vertical_layout)

        # Add file name
        file_name_label = QLabel(f"{file.name}")
        file_name_label.setStyleSheet("font-size: 20px;"
                                      f"font-family: {heading_font};"
                                      f"font-weight: bold;"
                                      f"text-transform: uppercase;")
        vertical_layout.addWidget(file_name_label)

        # Add file format
        file_format_label = QLabel(f"Format: {file.format}")
        file_format_label.setStyleSheet("font-size: 16px;"
                                        "margin-top: 10px;")
        vertical_layout.addWidget(file_format_label)


