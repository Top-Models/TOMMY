from PySide6.QtCore import Qt
from PySide6.QtWidgets import QHBoxLayout, QPushButton, QLabel

from tommy.controller.graph_controller import GraphController
from tommy.controller.publisher.publisher import Publisher
from tommy.support.constant_variables import (
    seco_col_blue, hover_seco_col_blue, pressed_seco_col_blue)


class PlotNavigationView(QLabel):
    """View containing buttons to navigate plots."""

    def __init__(self, graph_controller: GraphController) -> None:
        """Initialize the PlotNavigationView."""
        super().__init__()

        # Set reference to the graph-controller
        self._graph_controller = graph_controller

        # Initialize horizontal layout
        self.layout = QHBoxLayout()
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.setLayout(self.layout)

        # Initialize buttons
        self.next_plot_button = None
        self.previous_plot_button = None
        self.initialize_buttons()

    def initialize_buttons(self) -> None:
        """Initialize the buttons."""
        self.initialize_previous_plot_button()
        self.initialize_next_plot_button()

    def initialize_next_plot_button(self) -> None:
        """Initialize the next plot button."""
        self.next_plot_button = QPushButton(">")
        self.next_plot_button.setStyleSheet(
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
        self.next_plot_button.setFixedWidth(40)
        self.next_plot_button.setFixedHeight(40)
        self.layout.addWidget(self.next_plot_button)
        self.next_plot_button.clicked.connect(
            self.next_plot_button_clicked_event)

    def initialize_previous_plot_button(self) -> None:
        """Initialize the previous plot button."""
        self.previous_plot_button = QPushButton("<", self)
        self.previous_plot_button.setStyleSheet(
            f"""
                QPushButton {{
                    background-color: {seco_col_blue};
                    color: white;
                    border: none;
                }}
    
                QPushButton:hover {{
                    background-color: {hover_seco_col_blue};
                }}
    
                QPushButton:pressed {{
                    background-color: {pressed_seco_col_blue};
                }}
            """)
        self.previous_plot_button.setFixedWidth(40)
        self.previous_plot_button.setFixedHeight(40)
        self.layout.addWidget(self.previous_plot_button)
        self.previous_plot_button.clicked.connect(
            self.previous_plot_button_clicked_event)

    def next_plot_button_clicked_event(self) -> None:
        """Event handler for when the next plot button is clicked."""
        self._graph_controller.on_next_plot()

    def previous_plot_button_clicked_event(self) -> None:
        """Event handler for when the previous plot button is clicked."""
        self._graph_controller.on_previous_plot()


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University 
(Department of Information and Computing Sciences)
"""
