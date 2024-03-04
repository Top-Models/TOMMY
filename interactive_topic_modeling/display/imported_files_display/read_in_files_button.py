from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton

from interactive_topic_modeling.support import project_settings
from interactive_topic_modeling.backend.file_import.file_importer import FileImporter
import os


class ReadInFilesButton(QWidget):

    def __init__(self):
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
        files = self.file_reader.read_files()
        # Apply all other functions like preprocessing here

        print(list(files))


if __name__ == "__main__":
    print(globals())
