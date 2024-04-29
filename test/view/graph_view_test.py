import pytest
from PySide6.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.backends.backend_template import FigureCanvas
from matplotlib.figure import Figure
from pytestqt.qtbot import QtBot

from tommy.controller.graph_controller import GraphController
from tommy.view.graph_view import GraphView


@pytest.fixture(scope='function')
def graph_view(qtbot: QtBot) -> GraphView:
    graph_controller = GraphController()
    graph_view = GraphView(graph_controller)
    qtbot.addWidget(graph_view)
    return graph_view


def test_display_plot_layout_cleared_correctly(graph_view: GraphView):
    """
    Test if the layout is cleared correctly when displaying a plot.
    """
    # Create a canvas
    canvas = Figure()
    canvas.add_subplot(111)

    # Display the plot
    graph_view.display_plot(canvas)

    # Check if the layout was cleared
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
    graph_view.display_plot(canvas)

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
    graph_view.display_plot(canvas)

    # Check if the canvas was resized correctly
    assert canvas.subplotpars.left == 0.2
    assert canvas.subplotpars.bottom == 0.2
    assert canvas.subplotpars.right == 0.8
    assert canvas.subplotpars.top == 0.8


def test_display_plot_correlation_matrix(graph_view: GraphView):
    """
    Test displaying a correlation matrix plot.
    """
    # Create a canvas
    canvas = Figure()
    canvas.add_subplot(111, title="correlatiematrix")

    # Display the plot
    graph_view.display_plot(canvas)

    # Check if the canvas was resized correctly
    assert canvas.subplotpars.left == 0.3
    assert canvas.subplotpars.bottom == 0.2
    assert canvas.subplotpars.right == 0.7
    assert canvas.subplotpars.top == 0.8


def test_display_plot_default(graph_view: GraphView):
    """
    Test displaying a default plot.
    """
    # Create a canvas
    canvas = Figure()
    canvas.add_subplot(111)

    # Display the plot
    graph_view.display_plot(canvas)

    # Check if the canvas was resized correctly
    assert canvas.subplotpars.left == 0.1
    assert canvas.subplotpars.bottom == 0.1
    assert canvas.subplotpars.right == 0.9
    assert canvas.subplotpars.top == 0.9


def test_update_from_event(graph_view: GraphView):
    """
    Test updating the graph_view from an update of the eventhandler.
    """
    # create mock canvas
    canvas = Figure()
    canvas.add_subplot(111, title="gewicht")

    # simulate triggering of eventhandler
    graph_view._graph_controller.plots_changed_event.publish(canvas)

    # Check if the layout was cleared
    assert graph_view.layout.count() == 1


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University 
(Department of Information and Computing Sciences)
"""