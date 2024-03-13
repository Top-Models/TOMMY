from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton
import os

from interactive_topic_modeling.support import project_settings
from interactive_topic_modeling.backend.file_import.file_reader import (
    FileReader)


class ReadInFilesButton(QWidget):
    """
    The ReadInFilesButton class that defines the button to
    read in files.
    """
    def __init__(self) -> None:
        """Initialize the button."""
        super().__init__()

        self.file_reader = FileReader()

        # Initialize layout
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Initialize button
        btn = QPushButton("Read in files", self)
        btn.setToolTip("Start reading in files from the selected folder")
        btn.resize(btn.sizeHint())
        btn.move(150, 0)
        btn.clicked.connect(self.read_files)

    def read_files(self) -> None:
        """Read the files with the file reader."""
        files = self.file_reader.read_files()
        # Apply all other functions like preprocessing here

        print(list(files))


if __name__ == "__main__":
    print(globals())


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University 
(Department of Information and Computing Sciences)
"""
