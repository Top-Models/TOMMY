from PySide6.QtGui import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import (FigureCanvasQTAgg as
                                                FigureCanvas)
import matplotlib.figure


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

    def display_plot(self, canvas: matplotlib.figure.Figure) -> None:
        """
        Display the plots for the given tab.

        :param canvas: The canvas to display
        :return: None
        """

        # Clear the layout
        while self.layout.count():
            child = self.layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        # Set the DPI for the canvas
        canvas.figure.set_dpi(100)

        # Add the canvas to the layout
        self.layout.addWidget(FigureCanvas(canvas.figure))

    def clear_plot(self) -> None:
        """
        Clear the plot from the view.

        :return: None
        """
        self.display_plot(matplotlib.figure.Figure())


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University
(Department of Information and Computing Sciences)
"""
