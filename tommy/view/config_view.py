from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QPushButton, QInputDialog, QListWidget,
    QMessageBox, QListWidgetItem, QLabel, QHBoxLayout, QWidget
)

from tommy.controller.config_controller import ConfigController
from tommy.controller.model_parameters_controller import \
    ModelParametersController
from tommy.support.constant_variables import (heading_font, prim_col_red,
                                              hover_prim_col_red, text_font,
                                              medium_light_gray,
                                              hover_medium_light_gray,
                                              pressed_medium_light_gray,
                                              selected_medium_light_gray,
                                              seco_col_blue,
                                              hover_seco_col_blue,
                                              pressed_seco_col_blue)


class ConfigView(QDialog):
    """Widget for managing configurations"""

    def __init__(self, config_controller: ConfigController,
                 model_parameters_controller: ModelParametersController):
        super().__init__()
        self.config_controller = config_controller
        self.model_parameters_controller = model_parameters_controller
        self.setWindowTitle("Configuraties Beheer")
        self.setMaximumHeight(600)
        self.setMinimumHeight(400)
        self.setMinimumWidth(300)
        self.setMaximumWidth(400)

        self.layout = QVBoxLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)

        # Initialize title label
        self.title_label = None
        self.initialize_title_label()

        # List widget to display configurations
        self.config_list_widget = QListWidget()
        self.config_list_widget.setObjectName("list_widget")
        self.update_config_list()
        self.layout.addWidget(self.config_list_widget)

        # Buttons for configuration management
        self.buttons_container = QWidget()
        self.buttons_layout = QHBoxLayout()
        self.buttons_layout.setContentsMargins(0, 0, 0, 0)
        self.buttons_layout.setSpacing(0)
        self.buttons_container.setLayout(self.buttons_layout)
        self.layout.addWidget(self.buttons_container)

        button_stylesheet = f"""
                        QPushButton {{
                            background-color: {seco_col_blue};
                            color: white;
                            padding: 5px;
                            margin: 5px;
                        }}

                        QPushButton:hover {{
                            background-color: {hover_seco_col_blue};
                        }}

                        QPushButton:pressed {{
                            background-color: {pressed_seco_col_blue};
                        }}
                    """

        add_button = QPushButton("Toevoegen")
        add_button.clicked.connect(self.add_configuration)
        add_button.setStyleSheet(button_stylesheet)
        self.buttons_layout.addWidget(add_button)

        delete_button = QPushButton("Verwijderen")
        delete_button.clicked.connect(self.delete_configuration)
        delete_button.setStyleSheet(button_stylesheet)
        self.buttons_layout.addWidget(delete_button)

        load_button = QPushButton("Laden")
        load_button.clicked.connect(self.load_configuration)
        load_button.setStyleSheet(button_stylesheet)
        self.buttons_layout.addWidget(load_button)

        self.setLayout(self.layout)

        # Apply the stylesheet
        self.setStyleSheet(f"""
            background-color: white;
            font-size: 15px;
            font-family: '{text_font}', sans-serif;
            border: none;
        """)

        # Apply styling to the list widget
        self.config_list_widget.setStyleSheet(f"""
            QListWidget {{
                background-color: #f2f2f2;
                border: 1px solid #d9d9d9;
            }}

            QListWidget::item {{
                font-family: {text_font};
                font-size: 12px;
                background-color: {medium_light_gray};
                color: black;
                margin: 5px;
                padding: 3px;
            }}
            
            QListWidget::item:hover {{
                background-color: {hover_medium_light_gray};
            }}
            
            QListWidget::item:hover {{
                background-color: {pressed_medium_light_gray};
            }}

            QListWidget::item:selected {{
                background-color: {selected_medium_light_gray};
                color: #333333;
            }}
        """)

    def initialize_title_label(self) -> None:
        """
        Initialize the title label.

        :return: None
        """
        self.title_label = QLabel("Configuraties")
        self.title_label.setStyleSheet(f"font-size: 13px;"
                                       f"font-family: {heading_font};"
                                       f"font-weight: bold;"
                                       f"text-transform: uppercase;"
                                       f"background-color: {prim_col_red};"
                                       f"color: white;"
                                       f"border-bottom: "
                                       f"3px solid {hover_prim_col_red};")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter |
                                      Qt.AlignmentFlag.AlignTop)
        self.title_label.setContentsMargins(0, 0, 0, 0)
        self.title_label.setFixedHeight(50)
        self.layout.addWidget(self.title_label)

    def update_config_list(self):
        """Update the list of configurations"""
        self.config_list_widget.clear()
        configurations = self.config_controller.get_configuration_names()
        selected_config = self.config_controller.get_selected_configuration()
        for name in configurations:
            if name == selected_config:
                # TODO: change the style of this item to communicate to the
                #  user that this is the selected config
                item = QListWidgetItem(name)
                self.config_list_widget.addItem(item)
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
                # this happens when trying to add a configuration with a
                # name that already exists as a configuration
                QMessageBox.warning(self, "Fout bij toevoegen",
                                    "De configuratie kon niet worden "
                                    "toegevoegd")

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


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University 
(Department of Information and Computing Sciences)
"""
