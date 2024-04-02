from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QFileDialog
from tommy.controller.project_settings_controller import (
    ProjectSettingsController)
import os

from tommy.view.observer.observer import Observer


class FolderSelectButton(QWidget, Observer):
    """A button for selecting a folder containing input documents"""
    def __init__(self, project_settings_controller: ProjectSettingsController
                 ) -> None:
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

        self.project_settings_controller = project_settings_controller

    def select_folder(self) -> None:
        """Open a file dialog to select a folder."""
        dialog = QFileDialog.getExistingDirectory(self, "Select folder")
        if dialog:
            self.project_settings_controller.set_input_folder_path(
                os.path.relpath(dialog))

    def update_observer(self, publisher) -> None:
        """
        Update the observer.

        :param publisher: The publisher that is being observed
        :return: None
        """
        pass


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University 
(Department of Information and Computing Sciences)
"""
