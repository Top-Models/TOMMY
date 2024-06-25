import os

from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMenuBar, QWidget, QFileDialog, \
    QLabel, QDialog, QVBoxLayout, \
    QMessageBox

from tommy.controller.export_controller import ExportController
from tommy.controller.project_settings_controller import \
    ProjectSettingsController
from tommy.controller.saving_loading_controller import SavingLoadingController
from tommy.controller.topic_modelling_controller import \
    TopicModellingController
from tommy.support.constant_variables import (
    prim_col_red, dark_prim_col_red, extra_light_gray, text_font)
from tommy.view.error_view import ErrorView


class MenuBar(QMenuBar):
    """Menu bar class for the topic modelling application"""

    def __init__(self,
                 parent: QWidget,
                 project_settings_controller: ProjectSettingsController,
                 saving_loading_controller: SavingLoadingController,
                 export_controller: ExportController,
                 topic_modelling_controller: TopicModellingController
                 ) -> None:
        """Initialize the menu bar."""
        super().__init__(parent)

        # Set reference to project settings controller for input folder button
        self._project_settings_controller = project_settings_controller
        self._saving_loading_controller = saving_loading_controller
        self._export_controller = export_controller
        self._topic_modelling_controller = topic_modelling_controller

        # Subscribe to topic modelling controller
        self._topic_modelling_controller.start_training_model_event.subscribe(
                lambda _: self.disable_menu_on_start_topic_modelling())
        self._topic_modelling_controller.model_trained_event.subscribe(
                lambda _: self.enable_menu_on_finish_topic_modelling())

        # Create actions
        self.import_input_folder_action = (
            QAction("Selecteer input folder", self))
        self.export_to_gexf_action = QAction(
                "Exporteer naar Graph Exchange XML Format (.gexf)", self)
        self.export_to_png_action = QAction("Exporteer grafieken (.png)", self)
        self.export_topic_words_action = QAction("Exporteer Topicdata (.csv)",
                                                 self)
        self.export_document_topic_action = QAction(
                "Exporteer Document Topics (.csv)", self)
        self.save_settings_action = QAction("Instellingen opslaan", self)
        self.save_settings_as_action = QAction("Instellingen opslaan als",
                                               self)
        self.load_settings_action = QAction("Instellingen laden", self)
        self.info_action = QAction("Over TOMMY", self)

        # Connect actions to event handlers
        self.import_input_folder_action.triggered.connect(
            self.import_input_folder)
        self.export_to_gexf_action.triggered.connect(self.export_to_gexf)
        self.export_to_png_action.triggered.connect(self.export_to_png)
        self.export_topic_words_action.triggered.connect(
            self.export_topic_words)
        self.export_document_topic_action.triggered.connect(
                self.export_document_topics)
        self.save_settings_action.triggered.connect(self.save_settings_to_file)
        self.save_settings_as_action.triggered.connect(self.save_settings_as)
        self.load_settings_action.triggered.connect(
                self._load_settings_from_file)  # Connect to new method
        self.info_action.triggered.connect(self.show_about_dialog)

        # Create menu bar
        file_menu = self.addMenu("Bestand")
        file_menu.addAction(self.import_input_folder_action)
        file_menu.addAction(self.save_settings_action)
        file_menu.addAction(self.save_settings_as_action)
        file_menu.addAction(self.load_settings_action)

        # Add sub menu export_menu to menu bar
        export_menu = self.addMenu("Exporteren")
        export_menu.addAction(self.export_to_gexf_action)
        export_menu.addAction(self.export_to_png_action)
        export_menu.addAction(self.export_topic_words_action)
        export_menu.addAction(self.export_document_topic_action)

        # Create help bar
        help_menu = self.addMenu("Help")
        help_menu.addAction(self.info_action)

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

    def export_before_running(self) -> bool:
        """
        Raise an error if topic modelling is not yet performed and signal
        the method to stop
        :return: a boolean value whether the topic modelling is NOT
        yet perfomed
        """
        if not self._export_controller.is_topic_modelling_done():
            ErrorView("Topic modelling is nog niet uitgevoerd. "
                      "Klik op de knop 'toepassen' om het "
                      "programma uit te voeren.", [])
            return True
        return False

    def export_to_gexf(self) -> None:
        """
        Export the networks to GEXF files.
        :return: None
        """
        if self.export_before_running():
            return

        dialog = QFileDialog.getExistingDirectory(self,
                                                  "Selecteer export folder")

        if dialog:
            errors = self._export_controller.export_networks(dialog)
            if errors:
                ErrorView("Er is een fout opgetreden "
                          "bij het exporteren van de "
                          "netwerken.", errors)

    def export_to_png(self) -> None:
        """
        Export the plots to PNG files.
        :return: None
        """
        if self.export_before_running():
            return

        dialog = QFileDialog.getExistingDirectory(self,
                                                  "Selecteer export folder")

        if dialog:
            errors = self._export_controller.export_graphs(dialog)
            if errors:
                ErrorView("Er is een fout opgetreden "
                          "bij het exporteren van de "
                          "grafieken.", errors)

    def disable_menu_on_start_topic_modelling(self) -> None:
        """
        Disable the export menu when the topic modelling is started.
        :return: None
        """
        self.import_input_folder_action.setEnabled(False)

    def enable_menu_on_finish_topic_modelling(self) -> None:
        """
        Enable the export menu when the topic modelling is finished.
        :return: None
        """
        self.import_input_folder_action.setEnabled(True)

    def export_topic_words(self) -> None:
        """
        Export words related to topics to a CSV file.
        :return: None
        """
        if self.export_before_running():
            return

        dialog = QFileDialog.getSaveFileName(self, "Selecteer export locatie",
                                             filter="CSV files (*.csv)")

        if dialog[0]:
            export_path = dialog[0]
            errors = self._export_controller.export_topic_words_csv(
                    export_path)
            if errors:
                ErrorView("Er is een fout opgetreden bij "
                          "het exporteren van de "
                          "topics.", errors)

    def export_document_topics(self) -> None:
        """
        Export documents related to topics to a CSV file.
        :return: None
        """
        if self.export_before_running():
            return

        dialog = QFileDialog.getSaveFileName(self, "Selecteer export locatie",
                                             filter="CSV files (*.csv)")

        if dialog[0]:
            errors = self._export_controller.export_document_topics_csv(
                    dialog[0])
            if errors:
                ErrorView("Er is een fout opgetreden "
                          "bij het exporteren van het document.", errors)

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

    def show_about_dialog(self) -> None:
        """
        Show the About dialog.
        :return: None
        """
        about_dialog = AboutDialog(self)
        about_dialog.exec_()

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
        errors = self._saving_loading_controller.save_settings_to_file(
                filepath)
        if not errors:
            QMessageBox.information(self, "Project opgeslagen",
                                    "Het project is succesvol opgeslagen.")
        else:
            ErrorView("Er is een fout opgetreden bij het opslaan van het "
                      "project.", errors)

    def _load_settings_from_file(self) -> None:
        """
        Load project settings from a file selected by the user.
        :return: None
        """
        dialog = QFileDialog.getOpenFileName(self, "Selecteer bestand",
                                             filter="JSON files (*.json)")
        if dialog[0]:
            errors = self._saving_loading_controller.load_settings_from_file(
                    dialog[0])
            if not errors:
                QMessageBox.information(self, "Project geladen",
                                        "Het project is succesvol geladen.")
            else:
                ErrorView("Er is een fout opgetreden bij het laden van het "
                          "project.", errors)


class AboutDialog(QDialog):
    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Over")
        self.setMinimumSize(350, 150)

        layout = QVBoxLayout()
        label = QLabel("""
        <div style='text-align: center;'>
            <p>This program has been developed by students from the bachelor 
            Computer Science at Utrecht University within the Software 
            Project course.</p>
            <p>© Copyright Utrecht University<br/>
            (Department of Information and Computing Sciences)</p>
        </div>
        """)
        label.setWordWrap(True)
        layout.addWidget(label)
        self.setLayout(layout)


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University
(Department of Information and Computing Sciences)
"""
