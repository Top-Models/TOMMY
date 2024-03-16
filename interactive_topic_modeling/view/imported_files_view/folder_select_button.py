from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QFileDialog
from interactive_topic_modeling.support import project_settings
import os

from interactive_topic_modeling.view.observer.observer import Observer


class FolderSelectButton(QWidget, Observer):
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

    def update_observer(self, publisher) -> None:
        """
        Update the observer.

        :param publisher: The publisher that is being observed
        :return: None
        """
        pass


if __name__ == "__main__":
    print(globals())


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University 
(Department of Information and Computing Sciences)
"""
