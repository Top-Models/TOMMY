from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QFileDialog, \
    QHBoxLayout
from tommy.controller.project_settings_controller import (
    ProjectSettingsController)
import os

from tommy.support.constant_variables import (seco_col_blue,
                                              hover_seco_col_blue,
                                              pressed_seco_col_blue)


class FolderSelectButton(QWidget):
    """A button for selecting a folder containing input documents"""

    def __init__(self, project_settings_controller: ProjectSettingsController
                 ) -> None:
        super().__init__()
        """Initialize the FolderSelectButton widget."""

        # Initialize layout
        self.layout = QHBoxLayout()
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        # Initialize button
        btn = QPushButton("Selecteer folder", self)
        btn.setToolTip("Selecteer de folder die de input documenten bevat")
        self.setStyleSheet(
            f"""
                QPushButton {{
                    background-color: {seco_col_blue};
                    color: white;
                    text-align: center;
                    border: none;
                }}

                QPushButton:hover {{
                    background-color: {hover_seco_col_blue};
                }}

                QPushButton:pressed {{
                    background-color: {pressed_seco_col_blue};
                }}
            """)
        self.setFixedWidth(40)
        self.setFixedHeight(40)
        btn.clicked.connect(self.select_folder)
        self.layout.addWidget(btn)
        self.project_settings_controller = project_settings_controller

    def select_folder(self) -> None:
        """Open a file dialog to select a folder."""
        dialog = QFileDialog.getExistingDirectory(self, "Select folder")
        if dialog:
            # Publishing duties to inform people this has changed are done by
            # the controller
            self.project_settings_controller.set_input_folder_path(
                os.path.relpath(dialog))
        print(self.project_settings_controller.get_input_folder_path())


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University 
(Department of Information and Computing Sciences)
"""
