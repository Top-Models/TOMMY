import matplotlib.figure
import pytest
from PySide6.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.backends.backend_template import FigureCanvas
from matplotlib.figure import Figure
from pytestqt.qtbot import QtBot

from tommy.controller.graph_controller import GraphController
from tommy.controller.publisher.publisher import Publisher
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


def test_update_observer(graph_view: GraphView, mocker):
    """
    Test updating the observer.
    """
    # Mock the get_current_visualization method
    canvas = Figure()
    canvas.add_subplot(111, title="gewicht")
    mocker.patch.object(graph_view._graph_controller,
                        "get_current_visualization",
                        return_value=canvas)

    # Create a mock publisher
    mock_publisher = mocker.Mock(spec=Publisher)

    # Update the observer
    graph_view.update_observer(mock_publisher)

    # Check if the layout was cleared
    assert graph_view.layout.count() == 1
