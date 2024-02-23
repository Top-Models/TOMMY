from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QApplication
from PySide6 import QtGui
from pathlib import Path
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
        btn.clicked.connect(self.selectFolder)


    def selectFolder(self):
        dialog = QFileDialog.getExistingDirectory(self, "Select folder")
        print(os.path.relpath(dialog))

