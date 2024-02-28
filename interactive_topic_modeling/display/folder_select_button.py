from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QApplication
from PySide6 import QtGui
from pathlib import Path
from interactive_topic_modeling.support import project_settings
import os


class FolderSelectButton(QWidget):

    def __init__(self):
        super().__init__()

        # Initialize layout
        layout = QVBoxLayout()
        self.setLayout(layout)
        # Initialize button
        btn = QPushButton("Select folder", self)
        btn.setToolTip("Select the folder containing the input documents")
        btn.resize(btn.sizeHint())
        btn.clicked.connect(self.select_folder)

    def select_folder(self) -> None:
        dialog = QFileDialog.getExistingDirectory(self, "Select folder")
        project_settings.current_project_settings.selected_folder = (
            os.path.relpath(dialog))


if __name__ == "__main__":
    print(globals())
