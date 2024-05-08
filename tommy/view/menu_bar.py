import os

from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMenuBar, QMenu, QWidget, QFileDialog

from tommy.controller.export_controller import ExportController
from tommy.controller.project_settings_controller import (
    ProjectSettingsController)
from tommy.support.constant_variables import (
    prim_col_red, dark_prim_col_red, extra_light_gray, text_font)


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
        export_to_gexf_action = QAction("Exporteer naar Graph Exchange XML Format (.gexf)", self)
        export_to_png_action = QAction("Exporteer grafieken (.png)", self)
        export_topic_words_action = QAction("Exporteer onderwerpwijzer (.csv)", self)

        # Connect actions to event handlers
        import_input_folder_action.triggered.connect(self.import_input_folder)
        export_to_gexf_action.triggered.connect(self.export_to_gexf)
        export_to_png_action.triggered.connect(self.export_to_png)
        export_topic_words_action.triggered.connect(self.export_topic_words)

        # Create menu bar
        file_menu = self.addMenu("Bestand")
        file_menu.addAction(import_input_folder_action)

        # Add sub menu export_menu to menu bar
        export_menu = file_menu.addMenu("Exporteren")
        export_menu.addAction(export_to_gexf_action)
        export_menu.addAction(export_to_png_action)
        export_menu.addAction(export_topic_words_action)

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
        Export the networks to GEXF files.
        :return: None
        """
        dialog = QFileDialog.getExistingDirectory(self,
                                                  "Selecteer export folder")

        if dialog:
            self._export_controller.export_networks(dialog)

    def export_to_png(self) -> None:
        """
        Export the plots to PNG files.
        :return: None
        """
        dialog = QFileDialog.getExistingDirectory(self,
                                                  "Selecteer export folder")

        if dialog:
            self._export_controller.export_graphs(dialog)

    def export_topic_words(self) -> None:
        """
        Export words related to topics to a CSV file.
        :return: None
        """
        dialog = QFileDialog.getSaveFileName(self, "Selecteer export locatie",
                                             filter="CSV files (*.csv)")

        if dialog[0]:
            export_path = dialog[0]
            self._export_controller.export_topic_words_csv(export_path)


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University
(Department of Information and Computing Sciences)
"""
