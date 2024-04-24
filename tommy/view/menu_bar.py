import os

from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMenuBar, QMenu, QWidget, QFileDialog

from tommy.controller.export_controller import ExportController
from tommy.controller.project_settings_controller import (
    ProjectSettingsController)
from tommy.support.constant_variables import (
    prim_col_red, dark_prim_col_red, extra_light_gray, text_font)
from tommy.controller import export_controller


class MenuBar(QMenuBar):
    """Menu bar class for the topic modelling application"""

    def __init__(self,
                 parent: QWidget,
                 project_settings_controller: ProjectSettingsController,
                 export_controller: ExportController
                 ) -> None:
        """Initialize the menu bar."""
        super().__init__(parent)

        # Set reference to project settings controller for input folder button
        self._project_settings_controller = project_settings_controller

        self._export_controller = export_controller

        # Create actions
        import_input_folder_action = QAction("Selecteer input folder", self)
        export_action = QAction("Exporteren", self)

        # Create submenu for export
        export_to_gexf = QMenu(self)
        export_to_gexf.addAction("Graph Exchange XML Format (.gexf)")
        export_action.setMenu(export_to_gexf)

        # Connect actions to event handlers
        import_input_folder_action.triggered.connect(self.import_input_folder)
        export_to_gexf.triggered.connect(self.export_to_gexf)

        # Create menu bar
        file_menu = self.addMenu("Bestand")
        file_menu.addAction(import_input_folder_action)
        file_menu.addAction(export_action)

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
        dialog = QFileDialog.getExistingDirectory(self,
                                                  "Selecteer export folder")

        if dialog:
            self._export_controller.export_networks(dialog)




"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University 
(Department of Information and Computing Sciences)
"""
