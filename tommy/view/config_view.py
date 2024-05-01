from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QPushButton, QInputDialog, QListWidget,
    QMessageBox, QListWidgetItem
)
from PySide6.QtGui import QIcon, QColor, QBrush
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
        configurations = self.config_controller.get_configuration_names()
        selected_config = self.config_controller.get_selected_configuration()
        for name in configurations:
            if name == selected_config:
                item = QListWidgetItem(name)
                self.config_list_widget.addItem(item)
                print(f"The currently selected config is {name}")
            else:
                self.config_list_widget.addItem(name)

    def add_configuration(self):
        """Method to add a new configuration"""
        name, ok = QInputDialog.getText(self, "Voer Configuratie Naam In",
                                        "Naam:")
        if ok:
            success = self.config_controller.add_configuration(name)
            if success:
                self.update_config_list()
            else:
                QMessageBox.warning(self, "Fout bij toevoegen",
                                    "De configuratie kon niet worden "
                                    "toegevoegd")
            """
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
            """

    def delete_configuration(self):
        """Method to delete a configuration"""
        selected_items = self.config_list_widget.selectedItems()
        if selected_items:
            selected_item = selected_items[0]
            confirmation = QMessageBox.question(
                self, "Verwijder Configuratie",
                f"Weet u zeker dat u de configuratie "
                f"'{selected_item.text()}' wilt verwijderen?",
                QMessageBox.Yes | QMessageBox.No
            )
            if confirmation == QMessageBox.Yes:
                success = self.config_controller.delete_configuration(
                    selected_item.text())
                if success:
                    self.update_config_list()

    def load_configuration(self):
        """Method to load a configuration"""
        selected_items = self.config_list_widget.selectedItems()
        if selected_items:
            selected_item = selected_items[0]
            config_name = selected_item.text()
            success = self.config_controller.switch_configuration(config_name)
            if success:
                self.update_config_list()
            else:
                QMessageBox.warning(self, "Fout bij Laden",
                                    "Er is een fout opgetreden bij het "
                                    "laden van de configuratie.")

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
