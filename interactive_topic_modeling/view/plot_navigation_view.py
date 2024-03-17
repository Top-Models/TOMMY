from PySide6.QtCore import Qt
from PySide6.QtWidgets import QHBoxLayout, QPushButton, QLabel

from interactive_topic_modeling.backend.observer.publisher import Publisher
from interactive_topic_modeling.support.constant_variables import \
    seco_col_blue, hover_seco_col_blue, pressed_seco_col_blue
from interactive_topic_modeling.view.observer.observer import Observer


class PlotNavigationView(QLabel, Observer):
    """View containing buttons to navigate plots."""

    def __init__(self) -> None:
        """Initialize the PlotNavigationView."""
        super().__init__()

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

    # TODO: Implement when Connector is implemented
    def next_plot_button_clicked_event(self) -> None:
        """Event handler for when the next plot button is clicked."""
        pass

    # TODO: Implement when Connector is implemented
    def previous_plot_button_clicked_event(self) -> None:
        """Event handler for when the previous plot button is clicked."""
        pass

    def update_observer(self, publisher: Publisher) -> None:
        """
        Update the observer.

        :param publisher: The publisher that is being observed
        :return: None
        """
        pass


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University 
(Department of Information and Computing Sciences)
"""
