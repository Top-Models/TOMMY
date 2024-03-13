from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QFileDialog
from interactive_topic_modeling.support import project_settings
import os


class FolderSelectButton(QWidget):
    """A button for selecting a folder containing input documents"""
    def __init__(self) -> None:
        super().__init__()
        """Initialize the FolderSelectButton widget."""

        # Initialize layout
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Initialize button
        btn = QPushButton("Select folder", self)
        btn.setToolTip("Select the folder containing the input documents")
        btn.resize(btn.sizeHint())
        btn.clicked.connect(self.select_folder)

    def select_folder(self) -> None:
        """Open a file dialog to select a folder."""
        dialog = QFileDialog.getExistingDirectory(self, "Select folder")
        if dialog:
            project_settings.current_project_settings.selected_folder = (
                os.path.relpath(dialog))


if __name__ == "__main__":
    print(globals())
