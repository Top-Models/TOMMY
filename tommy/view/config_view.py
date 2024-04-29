from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QPushButton, QInputDialog, QListWidget,
    QMessageBox
)
from PySide6.QtGui import QIcon, QColor
from tommy.controller.config_controller import ConfigController
from tommy.model.config_model import ConfigModel
from tommy.controller.model_parameters_controller import \
    ModelParametersController
from tommy.support.constant_variables import text_font


class ConfigView(QDialog):
    """Widget for managing configurations"""

    def __init__(self, config_controller: ConfigController,
                 model_parameters_controller: ModelParametersController):
        super().__init__()
        self.config_controller = config_controller
        self.model_parameters_controller = model_parameters_controller
        self.setWindowTitle("Configuraties Beheer")

        layout = QVBoxLayout()

        # List widget to display configurations
        self.config_list_widget = QListWidget()
        self.update_config_list()
        layout.addWidget(self.config_list_widget)

        # Buttons for configuration management
        add_button = QPushButton("Configuratie Toevoegen")
        add_button.clicked.connect(self.add_configuration)
        layout.addWidget(add_button)

        delete_button = QPushButton("Configuratie Verwijderen")
        delete_button.clicked.connect(self.delete_configuration)
        layout.addWidget(delete_button)

        load_button = QPushButton("Configuratie Laden")
        load_button.clicked.connect(self.load_configuration)
        layout.addWidget(load_button)

        self.setLayout(layout)

        # Apply the stylesheet
        self.setStyleSheet("""
            background-color: white;
            font-size: 15px;
            font-family: 'Segoe UI', sans-serif;
            border: none;
        """)

        # Apply styling to the list widget
        self.config_list_widget.setStyleSheet("""
            QListWidget {
                background-color: #f2f2f2;
                border: 1px solid #d9d9d9;
            }

            QListWidget::item {
                background-color: #ffffff;
                padding: 5px;
                border-bottom: 1px solid #d9d9d9;
            }

            QListWidget::item:selected {
                background-color: #c1e2ff;
                color: #333333;
            }
        """)

    def update_config_list(self):
        """Update the list of configurations"""
        self.config_list_widget.clear()
        configurations = self.config_controller.list_configurations()
        for name in configurations:
            self.config_list_widget.addItem(name)

    def add_configuration(self):
        """Method to add a new configuration"""
        name, ok = QInputDialog.getText(self, "Voer Configuratie Naam In",
                                        "Naam:")
        if ok:
            # Create a new ConfigModel instance
            config = ConfigModel(name)
            # Set the parameters from the ModelParametersController
            config.model_parameters.n_topics = (
                self.model_parameters_controller.get_model_n_topics())
            config.model_parameters.model_type = (
                self.model_parameters_controller.get_model_type())
            # Add the configuration
            self.config_controller.add_configuration(name, config)
            self.update_config_list()

    def delete_configuration(self):
        """Method to delete a configuration"""
        selected_items = self.config_list_widget.selectedItems()
        if selected_items:
            selected_item = selected_items[0]
            confirmation = QMessageBox.question(
                self, "Verwijder Configuratie",
                f"Weet u zeker dat u de configuratie '{selected_item.text()}' wilt verwijderen?",
                QMessageBox.Yes | QMessageBox.No
            )
            if confirmation == QMessageBox.Yes:
                self.config_controller.delete_configuration(
                    selected_item.text())
                self.update_config_list()

    def load_configuration(self):
        """Method to load a configuration"""
        selected_items = self.config_list_widget.selectedItems()
        if selected_items:
            selected_item = selected_items[0]
            config_name = selected_item.text()
            config = self.config_controller.get_configuration(config_name)
            if config:
                # Update the model parameters view with the loaded configuration
                self.load_model_parameters(config)
                QMessageBox.information(self, "Configuratie Geladen",
                                        f"Configuratie '{config_name}' is succesvol geladen.")
            else:
                QMessageBox.warning(self, "Fout bij Laden",
                                    "Er is een fout opgetreden bij het laden van de configuratie.")

    def load_model_parameters(self, config: ConfigModel):
        """Method to load model parameters from a configuration"""
        model_parameters = config.model_parameters
        if model_parameters:
            # Set the loaded model parameters in the model parameters controller
            self.model_parameters_controller.set_model_n_topics(
                model_parameters.n_topics)
            self.model_parameters_controller.set_model_type(
                model_parameters.model_type)

"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University 
(Department of Information and Computing Sciences)
"""