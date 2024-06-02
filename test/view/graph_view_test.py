import pytest
from PySide6.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.backends.backend_template import FigureCanvas
from matplotlib.figure import Figure
from pytestqt.qtbot import QtBot

from tommy.view.graph_view import GraphView


@pytest.fixture(scope='function')
def graph_view(qtbot: QtBot) -> GraphView:
    graph_view = GraphView()
    qtbot.addWidget(graph_view)
    return graph_view


def test_display_plot_layout_cleared_correctly(graph_view: GraphView):
    """
    Test if the layout is cleared correctly when displaying a plot.
    """
    # Create two canvases
    canvas = Figure()
    canvas.add_subplot(111)
    canvas2 = Figure()
    canvas2.add_subplot(222)

    # Display plot 1
    graph_view.display_plot(canvas, "Woordaantal")

    # Display plot 2
    graph_view.display_plot(canvas2, "Woordaantal")

    # Check if the layout was cleared before displaying the second plot
    assert graph_view.layout.count() == 1
    assert isinstance(graph_view.layout.itemAt(0).widget(), FigureCanvasQTAgg)


def test_display_plot_dpi_set_correctly(graph_view: GraphView):
    """
    Test if the DPI is set correctly when displaying a plot.
    """
    # Create a canvas
    canvas = Figure()
    canvas.add_subplot(111)

    # Display the plot
    graph_view.display_plot(canvas, "Woordaantal")

    # Check if the DPI was set correctly
    assert canvas.figure.dpi == 100


def test_display_plot_weight(graph_view: GraphView):
    """
    Test displaying a weight plot.
    """
    # Create a canvas
    canvas = Figure()
    canvas.add_subplot(111, title="gewicht")

    # Display the plot
    graph_view.display_plot(canvas, "Woordaantal")

    # Check if the canvas was displayed
    assert graph_view.layout.count() == 1


def test_display_plot_correlation_matrix(graph_view: GraphView):
    """
    Test displaying a correlation matrix plot.
    """
    # Create a canvas
    canvas = Figure()
    canvas.add_subplot(111, title="correlatiematrix")

    # Display the plot
    graph_view.display_plot(canvas, "Woordaantal")

    # Check if the canvas was displayed
    assert graph_view.layout.count() == 1


def test_display_plot_default(graph_view: GraphView):
    """
    Test displaying a default plot.
    """
    # Create a canvas
    canvas = Figure()
    canvas.add_subplot(111)

    # Display the plot
    graph_view.display_plot(canvas, "Woordaantal")

    # Check if the canvas was displayed
    assert graph_view.layout.count() == 1


def test_clear_plot(graph_view: GraphView):
    """
    Test if the plot is cleared correctly.
    """
    # Create a canvas
    canvas = Figure()
    canvas.add_subplot(111)

    # Display the plot
    graph_view.display_plot(canvas, "Woordaantal")

    # Clear the plot
    graph_view.clear_plot()

    # Check if the plot was cleared
    assert graph_view.layout.count() == 1
    assert isinstance(graph_view.layout.itemAt(0).widget(), FigureCanvasQTAgg)


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University
(Department of Information and Computing Sciences)
"""