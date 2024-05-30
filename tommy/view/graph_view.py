from PySide6.QtGui import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import (FigureCanvasQTAgg as
                                                FigureCanvas)
import matplotlib.figure


def _resize_plot_for_type(canvas: matplotlib.figure.Figure,
                          visualization_type: str) -> None:
    """
    Resize the plot for the given type of visualization.

    :param canvas: The canvas to display
    :param visualization_type: The type of the visualization
    :return: None
    """
    if visualization_type == "Woordaantal":
        canvas.figure.subplots_adjust(left=0.2, right=0.8,
                                      top=0.85, bottom=0.25)
    elif visualization_type == "K-waarde":
        canvas.figure.subplots_adjust(left=0.2, right=0.8,
                                      top=0.85, bottom=0.25)
    elif visualization_type == "Woord Netwerk":
        canvas.figure.subplots_adjust(left=0.05, right=0.95,
                                      top=0.95, bottom=0.05)
    elif visualization_type == "Woordgewichten":
        canvas.figure.subplots_adjust(left=0.2, right=0.8,
                                      top=0.85, bottom=0.25)
    elif visualization_type == "Correlatie":
        canvas.figure.subplots_adjust(left=0.2, right=0.8,
                                      top=0.80, bottom=0.2)


class GraphView(QWidget):
    """A class for displaying the graphs made by the graph-controller"""

    def __init__(self) -> None:
        """Initialize the GraphDisplay."""
        super().__init__()

        # Set color of the widget to black
        self.setAutoFillBackground(True)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setStyleSheet("background-color: white;")

        # Setup layout
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.setMinimumHeight(350)
        self.setLayout(self.layout)

    def display_plot(self,
                     canvas: matplotlib.figure.Figure,
                     visualization_type: str) -> None:
        """
        Display the plots for the given tab.

        :param canvas: The canvas to display
        :param visualization_type: The type of the visualization
        :return: None
        """

        # Clear the layout
        while self.layout.count():
            child = self.layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        # Set the DPI for the canvas
        canvas.figure.set_dpi(100)

        # Resize the plot for the given type
        _resize_plot_for_type(canvas, visualization_type)

        # Add the canvas to the layout
        self.layout.addWidget(FigureCanvas(canvas.figure))

    def clear_plot(self) -> None:
        """
        Clear the plot from the view.

        :return: None
        """
        self.display_plot(matplotlib.figure.Figure(),
                          visualization_type="")


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University
(Department of Information and Computing Sciences)
"""
