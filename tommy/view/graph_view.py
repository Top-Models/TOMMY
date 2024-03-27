import matplotlib.figure
from PySide6.QtGui import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import (FigureCanvasQTAgg as
                                                FigureCanvas)

from tommy.backend.observer.publisher import Publisher
from tommy.view.observer.observer import Observer


class GraphView(QWidget, Observer):
    """A class for displaying the graphs made by topic modelling"""

    def __init__(self) -> None:
        """Initialize the GraphDisplay."""
        super().__init__()

        # Set color of the widget to black
        self.setAutoFillBackground(True)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setStyleSheet("background-color: black;")

        # Setup layout
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.setLayout(self.layout)

    def display_plot(self, canvas: matplotlib.figure.Figure) -> None:
        """
        Display the plots for the given tab.

        :param canvas: The canvas to display
        :return: None
        """

        # Clear the layout
        for i in reversed(range(self.layout.count())):
            self.layout.itemAt(i).widget().setParent(None)

        # Set the DPI for the canvas
        canvas.figure.set_dpi(100)

        # Resize canvas based on plot type
        plot_type = canvas.figure.axes[0].get_title().lower()
        if plot_type.__contains__("gewicht"):
            canvas.figure.subplots_adjust(0.3, 0.2, 0.9, 0.8)
        else:
            canvas.figure.subplots_adjust(0.1, 0.1, 0.9, 0.9)

        # Add the canvas to the layout
        self.layout.addWidget(FigureCanvas(canvas.figure))

    def update_observer(self, publisher: Publisher) -> None:
        """
        Update the view.

        :param publisher: The publisher to update the view from
        :return: None
        """
        pass


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University 
(Department of Information and Computing Sciences)
"""
