from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QLabel, QScrollArea, QVBoxLayout, QLayout,
                               QWidget, QSizePolicy, QPushButton, QGridLayout)

from tommy.controller.graph_controller import GraphController
from tommy.controller.model_parameters_controller import (
    ModelParametersController)
from tommy.support.constant_variables import (
    heading_font,
    prim_col_red, hover_prim_col_red, scrollbar_style, text_font,
    title_label_font, settings_label_font, file_name_label_font,
    file_property_font, no_component_selected_font, topic_title_font,
    topic_word_font, collapse_button_font)
from tommy.view.imported_files_view.file_label import FileLabel


class SelectedInformationView(QScrollArea):
    """Class to define the SelectedInformationView UI component"""

    def __init__(self,
                 graph_controller: GraphController,
                 model_parameters_controller: ModelParametersController
                 ) -> None:
        """Initialize the SelectedInformationView."""
        super().__init__()

        # Initialize widget properties
        self.setStyleSheet(f"background-color: white;"
                           f"color: black;"
                           f"font-family: {text_font};")
        self.setMinimumHeight(200)
        self.setMaximumHeight(300)

        # Initialize layout
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.layout.setSpacing(0)
        self.setLayout(self.layout)

        # Add title widget with collapse button
        self.title_widget = None
        self.initialize_title_widget()

        # Initialize scroll area and its layout
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_widget)
        self.scroll_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.scroll_area.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scroll_area.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll_area.setWidget(self.scroll_widget)
        self.scroll_area.setStyleSheet(scrollbar_style)
        self.layout.addWidget(self.scroll_area)

        # Initialize controllers
        self._graph_controller = graph_controller
        self._model_parameters_controller = model_parameters_controller

        # Initialize widgets
        self.display_no_component_selected()

        # Set size policy
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setMinimumWidth(0)  # Allow the widget to shrink to zero width

    def initialize_title_widget(self) -> None:
        """
        Add the title label widget with collapse button
        """
        self.title_widget = QWidget()
        self.title_widget.setFixedHeight(50)

        # Initialize layout for the title widget
        title_layout = QGridLayout(self.title_widget)
        title_layout.setContentsMargins(0, 0, 0, 0)
        title_layout.setSpacing(0)

        # Create the title label
        self.title_widget.title_label = QLabel("Informatie")
        self.title_widget.title_label.setStyleSheet(f"font-size: 13px;"
                                  f"font-family: {heading_font};"
                                  f"font-weight: bold;"
                                  f"text-transform: uppercase;"
                                  f"background-color: {prim_col_red};"
                                  f"color: white;"
                                  f"border-bottom: "
                                  f"3px solid {hover_prim_col_red};"
                                  f"border-left: 2px solid "
                                  f"{hover_prim_col_red};")
        self.title_widget.title_label.setContentsMargins(0, 0, 0, 0)
        self.title_widget.title_label.setFixedHeight(50)
        self.title_widget.title_label.setFont(title_label_font)
        self.title_widget.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Create the collapse button
        self.title_widget.title_button = QPushButton("▽")
        self.title_widget.title_button.setStyleSheet(f"font-size: 13px;"
                                        f"font-family: {heading_font};"
                                        f"font-weight: bold;"
                                        f"text-transform: uppercase;"
                                        f"background-color: {prim_col_red};"
                                        f"color: white;"
                                        f"border-bottom: "
                                        f"3px solid {hover_prim_col_red};"
                                        "}"
                                        "QPushButton:hover {"
                                        f"background-color: {hover_prim_col_red};")
        self.title_widget.title_button.setFixedSize(50, 50)

        # Add the title label and button to the layout
        title_layout.addWidget(self.title_widget.title_label, 0, 1)
        title_layout.addWidget(self.title_widget.title_button, 0, 2)
        self.layout.addWidget(self.title_widget)

        self.title_widget.title_button.setFont(collapse_button_font)
        self.title_widget.title_button.clicked.connect(self.toggle_collapse_info)

        # Add title widget to main layout
        self.layout.addWidget(self.title_widget)

    def toggle_collapse_info(self) -> None:
        """
        Toggle visibility of the scroll area and adjust layout accordingly.
        """
        self.collapse_component_info()
        self.change_button_appearance_info()

    def change_button_appearance_info(self) -> None:
        """
        Change the appearance of the toggle button.
        """
        if self.scroll_area.isVisible():
            self.title_widget.title_button.setText("▽")
        else:
            self.title_widget.title_button.setText("△")

    def collapse_component_info(self) -> None:
        """
        Collapse the information view.
        """
        if self.scroll_area.isVisible():
            # Hide the scroll area
            self.scroll_area.setVisible(False)
            # Move the header to the bottom of the layout
            self.layout.addStretch(0.1)
            self.layout.addWidget(self.title_widget)
            # Fix widget size to allow entire layout to be moved to
            self.setFixedHeight(self.title_widget.height())
        else:
            # Show the scroll area
            self.scroll_area.setVisible(True)

            # Remove the stretch from the layout to move the header
            # back to its original position
            self.layout.removeWidget(self.title_widget)
            self.layout.insertWidget(0, self.title_widget)
            self.layout.removeItem(self.layout.itemAt(self.layout.count() - 1))

            # Restore beginning height
            self.setMinimumHeight(200)
            self.setMaximumHeight(300)

    def display_no_component_selected(self) -> None:
        """
        Display a message when no component is selected.
        :return: None
        """
        # Prepare layout
        self.clear_layout()
        self.scroll_layout.setContentsMargins(0, 0, 0, 0)

        # Set scroll layout align center
        self.scroll_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Add label
        no_file_selected_label = QLabel("Geen component\ngeselecteerd")
        no_file_selected_label.setFont(no_component_selected_font)
        no_file_selected_label.setStyleSheet("font-size: 20px;"
                                             f"font-family: {text_font};")
        no_file_selected_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.scroll_layout.addWidget(no_file_selected_label)

    def clear_layout(self) -> None:
        """
        Clear the layout.
        :return: None
        """
        self.clear_sub_layout(self.scroll_layout)

    def clear_sub_layout(self, layout: QLayout) -> None:
        """
        Clear a sub-layout
        :param layout: The sub-layout to clear
        :return: None
        """
        while layout.count() > 0:
            item = layout.takeAt(0)
            if item:
                widget = item.widget()
                if widget:
                    widget.deleteLater()
                else:
                    self.clear_sub_layout(item.layout())

    def display_file_info(self, file_label: FileLabel) -> None:
        """
        Display the file info
        :param file_label: The file label to display
        :return: None
        """

        if not file_label.selected:
            self.display_no_component_selected()
            return

        file_metadata = file_label.file

        # Prepare layout
        self.clear_layout()

        # Set scroll layout align top left
        self.scroll_layout.setAlignment(Qt.AlignmentFlag.AlignTop |
                                        Qt.AlignmentFlag.AlignLeft)

        # Use a vertical layout
        vertical_layout = QVBoxLayout()
        vertical_layout.setAlignment(Qt.AlignmentFlag.AlignTop |
                                     Qt.AlignmentFlag.AlignLeft)

        # Adjust the left margin here
        vertical_layout.setContentsMargins(20, 20, 0, 10)
        vertical_layout.setSpacing(10)
        self.scroll_layout.addLayout(vertical_layout)

        # Add file name
        file_name = file_metadata.name.split("/")[-1]
        file_name_label = QLabel(f"{file_name}")
        file_name_label.setStyleSheet(f"font-weight: bold;"
                                      f"text-transform: uppercase;")
        file_name_label.setFont(file_name_label_font)
        file_name_label.setAlignment(Qt.AlignmentFlag.AlignLeft |
                                     Qt.AlignmentFlag.AlignTop)
        file_name_label.setMinimumHeight(30)
        vertical_layout.addWidget(file_name_label)

        # Add file path
        file_path_label = QLabel(f"Pad: {file_metadata.path}")
        file_path_label.setFont(file_property_font)
        file_path_label.setStyleSheet("font-size: 16px;")
        file_path_label.setAlignment(Qt.AlignmentFlag.AlignLeft |
                                     Qt.AlignmentFlag.AlignTop)
        file_path_label.setMinimumHeight(20)
        vertical_layout.addWidget(file_path_label)

        # Add file format
        file_format_label = QLabel(f"Formaat: {file_metadata.format}")
        file_format_label.setFont(file_property_font)
        file_format_label.setStyleSheet("font-size: 16px;")
        file_format_label.setAlignment(Qt.AlignmentFlag.AlignLeft |
                                       Qt.AlignmentFlag.AlignTop)
        file_format_label.setMinimumHeight(20)
        vertical_layout.addWidget(file_format_label)

        # Add word amount
        word_amount_label = QLabel(f"Aantal woorden: {file_metadata.length}")
        word_amount_label.setFont(file_property_font)
        word_amount_label.setStyleSheet("font-size: 16px;")
        word_amount_label.setAlignment(Qt.AlignmentFlag.AlignLeft |
                                       Qt.AlignmentFlag.AlignTop)
        word_amount_label.setMinimumHeight(20)
        vertical_layout.addWidget(word_amount_label)

        # Add file size
        file_size_label = QLabel(f"Grootte: {file_metadata.size}B")
        file_size_label.setFont(file_property_font)
        file_size_label.setStyleSheet("font-size: 16px;")
        file_size_label.setAlignment(Qt.AlignmentFlag.AlignLeft |
                                     Qt.AlignmentFlag.AlignTop)
        file_size_label.setMinimumHeight(20)
        vertical_layout.addWidget(file_size_label)

    def display_topic_info(self, topic_entity) -> None:
        """
        Display the topic information
        :param topic_entity: The topic entity to display
        :return: None
        """

        if not topic_entity.selected:
            self.display_no_component_selected()
            return

        # Prepare layout
        self.clear_layout()

        # Set scroll layout align top left
        self.scroll_layout.setAlignment(Qt.AlignmentFlag.AlignTop |
                                        Qt.AlignmentFlag.AlignLeft)

        # Use a vertical layout
        vertical_layout = QVBoxLayout()
        vertical_layout.setAlignment(Qt.AlignmentFlag.AlignTop |
                                     Qt.AlignmentFlag.AlignLeft)

        # Adjust the left margin here
        vertical_layout.setContentsMargins(20, 20, 0, 10)
        vertical_layout.setSpacing(10)
        self.scroll_layout.addLayout(vertical_layout)

        # Add topic name
        topic_name = topic_entity.topic_name
        topic_name_label = QLabel(f"{topic_name}")
        topic_name_label.setFont(topic_title_font)
        topic_name_label.setStyleSheet(f"font-size: 18px;"
                                       f"font-family: {heading_font};"
                                       f"font-weight: bold;"
                                       f"text-transform: uppercase;")
        topic_name_label.setAlignment(Qt.AlignmentFlag.AlignLeft |
                                      Qt.AlignmentFlag.AlignTop)
        topic_name_label.setMinimumHeight(20)
        vertical_layout.addWidget(topic_name_label)

        # Add words
        for word_entity in topic_entity.word_entities:
            word_label = QLabel(f"{word_entity.word}")
            word_label.setStyleSheet(f"font-size: 16px;")
            word_label.setFont(topic_word_font)
            word_label.setAlignment(Qt.AlignmentFlag.AlignLeft |
                                    Qt.AlignmentFlag.AlignTop)
            # Make sure word_label is always big enough
            word_label.setMinimumHeight(20)
            vertical_layout.addWidget(word_label)

    def display_run_info(self, run_name: str) -> None:
        """
        Display the run information

        :param run_name: The name of the run
        :return: None
        """

        # Display no component selected if no run is available
        try:
            topic_amount: int = (
                self._graph_controller.get_number_of_topics())
            model_type: str = (
                self._graph_controller.get_model_type())
        except RuntimeError:
            self.display_no_component_selected()
            return

        # Prepare layout
        self.clear_layout()

        # Set scroll layout align top left
        self.scroll_layout.setAlignment(Qt.AlignmentFlag.AlignTop |
                                        Qt.AlignmentFlag.AlignLeft)

        # Use a vertical layout
        vertical_layout = QVBoxLayout()
        vertical_layout.setAlignment(Qt.AlignmentFlag.AlignTop |
                                     Qt.AlignmentFlag.AlignLeft)

        # Adjust the left margin here
        vertical_layout.setContentsMargins(20, 20, 0, 10)
        vertical_layout.setSpacing(10)
        self.scroll_layout.addLayout(vertical_layout)

        # Add run name
        run_name_label = QLabel(f"{run_name}")
        run_name_label.setStyleSheet(f"font-size: 18px;"
                                     f"font-family: {heading_font};"
                                     f"font-weight: bold;"
                                     f"text-transform: uppercase;")
        run_name_label.setFont(settings_label_font)
        run_name_label.setAlignment(Qt.AlignmentFlag.AlignLeft |
                                    Qt.AlignmentFlag.AlignTop)
        run_name_label.setMinimumHeight(20)
        vertical_layout.addWidget(run_name_label)

        # Display model type
        model_type_label = QLabel(f"Model type: {model_type}")
        model_type_label.setStyleSheet("font-size: 16px;")
        model_type_label.setFont(settings_label_font)
        model_type_label.setAlignment(Qt.AlignmentFlag.AlignLeft |
                                      Qt.AlignmentFlag.AlignTop)
        model_type_label.setMinimumHeight(20)
        vertical_layout.addWidget(model_type_label)

        # Display topic amount
        topic_amount_label = QLabel(f"Aantal topics: {topic_amount}")
        topic_amount_label.setFont(settings_label_font)
        topic_amount_label.setStyleSheet("font-size: 16px;")
        topic_amount_label.setAlignment(Qt.AlignmentFlag.AlignLeft |
                                        Qt.AlignmentFlag.AlignTop)
        topic_amount_label.setMinimumHeight(20)
        vertical_layout.addWidget(topic_amount_label)


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University
(Department of Information and Computing Sciences)
"""
