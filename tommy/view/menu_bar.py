import os

from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMenuBar, QMenu, QWidget, QFileDialog

from tommy.controller.project_settings_controller import (
    ProjectSettingsController)
from tommy.support.constant_variables import (
    prim_col_red, dark_prim_col_red, extra_light_gray, text_font)


class MenuBar(QMenuBar):
    """Menu bar class for the topic modelling application"""

    def __init__(self,
                 parent: QWidget,
                 project_settings_controller: ProjectSettingsController
                 ) -> None:
        """Initialize the menu bar."""
        super().__init__(parent)

        # Set reference to project settings controller for input folder button
        self._project_settings_controller = project_settings_controller

        # Create actions
        import_input_folder_action = QAction("Selecteer input folder", self)
        export_action = QAction("Exporteren", self)
        save_settings_action = QAction("Instellingen opslaan", self)
        load_settings_action = QAction("Instellingen laden", self)  # New action for loading settings

        # Create submenu for export
        export_to_gexf = QMenu(self)
        export_to_gexf.addAction("Graph Exchange XML Format (.gexf)")
        export_action.setMenu(export_to_gexf)

        # Connect actions to event handlers
        import_input_folder_action.triggered.connect(self.import_input_folder)
        export_to_gexf.triggered.connect(self.export_to_gexf)
        save_settings_action.triggered.connect(self.save_settings_to_file)
        load_settings_action.triggered.connect(self.load_settings_from_file)  # Connect to new method

        # Create menu bar
        file_menu = self.addMenu("Bestand")
        file_menu.addAction(import_input_folder_action)
        file_menu.addAction(export_action)
        file_menu.addAction(save_settings_action)
        file_menu.addAction(load_settings_action)  # Add the new action to the menu

        # Set style
        self.setStyleSheet(f"""
            QMenuBar {{
                background-color: {prim_col_red};
                color: {extra_light_gray};
                font-family: {text_font};
            }}
            QMenuBar::item {{
                background-color: {dark_prim_col_red};
            }}
            QMenuBar::item:selected {{
                background-color: {extra_light_gray};
                color: {prim_col_red};
            }}
            QMenuBar::item:pressed {{
                background-color: {extra_light_gray};
                color: {prim_col_red};
            }}
            QMenu {{
                background-color: {prim_col_red};
                color: {extra_light_gray};
            }}
            QMenu::item:selected {{
                background-color: {extra_light_gray};
                color: {prim_col_red};
            }}
        """)

    def import_input_folder(self) -> None:
        """
        Open a file dialog to select a folder and set input folder in
        project settings
        :return: None
        """
        dialog = QFileDialog.getExistingDirectory(self,
                                                  "Selecteer input folder")
        if dialog:
            # Publishing duties to inform people this has changed are done by
            # the controller
            self._project_settings_controller.set_input_folder_path(
                os.path.relpath(dialog))

    def export_to_gexf(self) -> None:
        """
        Export the current graph to a GEXF file.

        :return: None
        """
        pass

    def save_settings_to_file(self) -> None:
        """
        Save project settings to a file.
        :return: None
        """
        file_path, _ = QFileDialog.getSaveFileName(self,
                                                   "Instellingen opslaan", "",
                                                   "JSON Files (*.json)")
        if file_path:
            self._project_settings_controller.save_settings_to_file(file_path)

    def load_settings_from_file(self) -> None:
        """
        Load project settings from a file.
        :return: None
        """
        file_path, _ = QFileDialog.getOpenFileName(self, "Instellingen laden",
                                                   "", "JSON Files (*.json)")
        if file_path:
            self._project_settings_controller.load_settings_from_file(
                file_path)

"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University 
(Department of Information and Computing Sciences)
"""
