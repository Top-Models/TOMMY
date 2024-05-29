import os

from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMenuBar, QWidget, QFileDialog, QMessageBox

from tommy.controller.export_controller import ExportController
from tommy.controller.project_settings_controller import \
    ProjectSettingsController
from tommy.controller.saving_loading_controller import SavingLoadingController
from tommy.support.constant_variables import (
    prim_col_red, dark_prim_col_red, extra_light_gray, text_font)


class MenuBar(QMenuBar):
    """Menu bar class for the topic modelling application"""

    def __init__(self,
                 parent: QWidget,
                 project_settings_controller: ProjectSettingsController,
                 saving_loading_controller: SavingLoadingController,
                 export_controller: ExportController
                 ) -> None:
        """Initialize the menu bar."""
        super().__init__(parent)

        # Set reference to project settings controller for input folder button
        self._project_settings_controller = project_settings_controller
        self._saving_loading_controller = saving_loading_controller

        self._export_controller = export_controller

        # Create actions
        import_input_folder_action = QAction("Selecteer input folder", self)
        export_to_gexf_action = QAction(
            "Exporteer naar Graph Exchange XML Format (.gexf)", self)
        export_to_png_action = QAction("Exporteer grafieken (.png)", self)
        export_topic_words_action = QAction("Exporteer Topicdata (.csv)", self)
        save_settings_action = QAction("Instellingen opslaan", self)
        save_settings_as_action = QAction("Instellingen opslaan als", self)
        load_settings_action = QAction("Instellingen laden", self)

        # Connect actions to event handlers
        import_input_folder_action.triggered.connect(self.import_input_folder)
        export_to_gexf_action.triggered.connect(self.export_to_gexf)
        export_to_png_action.triggered.connect(self.export_to_png)
        export_topic_words_action.triggered.connect(self.export_topic_words)
        save_settings_action.triggered.connect(self.save_settings_to_file)
        save_settings_as_action.triggered.connect(self.save_settings_as)
        load_settings_action.triggered.connect(
            self.load_settings_from_file)  # Connect to new method

        # Create menu bar
        file_menu = self.addMenu("Bestand")
        file_menu.addAction(import_input_folder_action)
        file_menu.addAction(save_settings_action)
        file_menu.addAction(save_settings_as_action)
        file_menu.addAction(load_settings_action)

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

    def save_settings_to_file(self) -> None:
        """
        Save project settings to a file. If the file path is not already
        known, the user is asked by calling save_settings_as instead.
        :return: None
        """
        if self._saving_loading_controller.filepath:
            self._save_settings_and_show_dialog(
                self._saving_loading_controller.filepath)
        else:
            self.save_settings_as()

    def save_settings_as(self) -> None:
        """
        Ask the user where to save the project settings and save them.
        :return: None
        """
        dialog = QFileDialog.getSaveFileName(self, "Selecteer opslaglocatie",
                                             filter="JSON files (*.json)")
        if dialog[0]:
            self._save_settings_and_show_dialog(dialog[0])

    def _save_settings_and_show_dialog(self, filepath) -> None:
        """
        Save the project settings to a file and show a dialog to show the
        user whether file saving succeeded or not.
        :param filepath: The filepath where the settings should be saved
        :return: None
        """
        if self._saving_loading_controller.save_settings_to_file(filepath):
            QMessageBox.information(self, "Project opgeslagen",
                                    "Het project is succesvol opgeslagen.")
        else:
            QMessageBox.critical(self, "Fout",
                                 "Er is een fout opgetreden bij het opslaan "
                                 "van het project.")

    def load_settings_from_file(self) -> None:
        """
        Load project settings from a file selected by the user.
        :return: None
        """
        dialog = QFileDialog.getOpenFileName(self, "Selecteer bestand",
                                             filter="JSON files (*.json)")
        if dialog[0]:
            if self._saving_loading_controller.load_settings_from_file(
                    dialog[0]):
                QMessageBox.information(self, "Project geladen",
                                        "Het project is succesvol geladen.")
            else:
                QMessageBox.critical(self, "Fout",
                                     "Er is een fout opgetreden bij het "
                                     "laden van het project.")


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University
(Department of Information and Computing Sciences)
"""
