from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QScrollArea, QVBoxLayout, QLayout

from interactive_topic_modeling.backend.file_import.file import File
from interactive_topic_modeling.support.constant_variables import seco_col_blue, heading_font


class FileStatsDisplay(QScrollArea):

    def __init__(self):
        super().__init__()

        # Initialize widget properties
        self.setStyleSheet(f"background-color: {seco_col_blue};")

        # Initialize layout
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Initialize widgets
        self.display_no_file_selected()

    def display_no_file_selected(self) -> None:
        """
        Display a message when no file is selected
        :return: None
        """

        # Prepare layout
        self.clear_layout()
        self.layout.setContentsMargins(0, 0, 0, 0)

        # Add label
        no_file_selected_label = QLabel("No file selected")
        no_file_selected_label.setStyleSheet("font-size: 20px;")
        no_file_selected_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(no_file_selected_label)

    def clear_layout(self) -> None:
        """
        Clear the layout
        :return: None
        """
        while self.layout.count() > 0:
            item = self.layout.takeAt(0)
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
        vertical_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        vertical_layout.setContentsMargins(20, 20, 0, 0)  # Adjust the left margin here
        vertical_layout.setSpacing(10)
        self.layout.addLayout(vertical_layout)

        # Add file name
        file_name_label = QLabel(f"{file.name}")
        file_name_label.setStyleSheet("font-size: 20px;"
                                      f"font-family: {heading_font};"
                                      f"font-weight: bold;"
                                      f"text-transform: uppercase;")
        file_name_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        vertical_layout.addWidget(file_name_label)

        # Add file format
        file_format_label = QLabel(f"Format: {file.format}")
        file_format_label.setStyleSheet("font-size: 16px;"
                                        "margin-top: 10px;")
        file_format_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        vertical_layout.addWidget(file_format_label)

        print(self.layout.count())




