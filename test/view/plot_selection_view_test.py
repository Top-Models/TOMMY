import pytest
from PySide6.QtWidgets import QWidget
from pytest_mock import MockerFixture
from pytestqt.qtbot import QtBot
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

from tommy.controller.controller import Controller
from tommy.view.plot_selection_view import (PlotSelectionView,
                                            PossibleVisualization,
                                            VisGroup)
from tommy.view.graph_view import GraphView
from test.helper_fixtures import controller_no_pipeline


@pytest.fixture
def controller(controller_no_pipeline):
    return controller_no_pipeline


@pytest.fixture(scope='function')
def plot() -> Figure:
    canvas = Figure()
    canvas.add_subplot(111)
    plt.close()
    return canvas


@pytest.fixture(scope='function')
def plot_selection_view(qtbot: QtBot, controller) -> PlotSelectionView:
    plot_selection_view = PlotSelectionView(
        controller.graph_controller,
        controller.config_controller,
        GraphView(),
    )
    qtbot.addWidget(plot_selection_view)
    return plot_selection_view


@pytest.mark.parametrize("input_visualizations, expected_visualization_count",
                         [
                             ([], 0),
                             ([PossibleVisualization(0, "str", "s",
                                                     VisGroup.TOPIC, False)],
                              1),
                             ([PossibleVisualization(3, "at", "sto",
                                                     VisGroup.CORPUS, True),
                               PossibleVisualization(2, "n2", "2",
                                                     VisGroup.CORPUS, True)],
                              2),
                             ([PossibleVisualization(3, "very long name",
                                                     "long name",
                                                     VisGroup.MODEL, False),
                               PossibleVisualization(5, "", "", VisGroup.TOPIC,
                                                     True),
                               PossibleVisualization(7, "1", "2",
                                                     VisGroup.CORPUS, False)],
                              5)
                         ])
def test_create_tabs_from_publisher(plot: Figure,
                                    plot_selection_view: PlotSelectionView,
                                    input_visualizations:
                                    list[PossibleVisualization],
                                    expected_visualization_count,
                                    mocker):
    # Define a mock function for get_visualization
    def mock_get_visualization(_):
        return plot, "plot_type"

    # Patch the get_visualization method with the mock
    mocker.patch.object(plot_selection_view._graph_controller,
                        'get_visualization',
                        side_effect=mock_get_visualization)

    # Act - trigger event and send possible visualizations
    plot_selection_view._graph_controller.possible_plots_changed_event.publish(
        input_visualizations)

    # Assert - check if the visualizations are created
    assert plot_selection_view.count() == expected_visualization_count


@pytest.mark.parametrize("input_visualizations, index_to_click, "
                         "expected_index_of_plot",
                         [
                             ([], 0, None),
                             ([PossibleVisualization(0, "str", "s",
                                                     VisGroup.TOPIC, False)],
                              0, None),
                             ([PossibleVisualization(3, "at", "sto",
                                                     VisGroup.CORPUS, True),
                               PossibleVisualization(2, "n2", "2",
                                                     VisGroup.CORPUS, True)],
                              1, 2),
                             ([PossibleVisualization(3, "very long name",
                                                     "long name",
                                                     VisGroup.CORPUS, False),
                               PossibleVisualization(5, "", "", VisGroup.MODEL,
                                                     True),
                               PossibleVisualization(7, "1", "2",
                                                     VisGroup.TOPIC, False)],
                              4, 7)
                         ])
def test_tab_clicked_event(plot: Figure,
                           plot_selection_view: PlotSelectionView,
                           input_visualizations:
                           list[PossibleVisualization],
                           index_to_click: int, expected_index_of_plot: int):
    requested_plots = []
    # Mock graph_retrieval from graph_controller and graph view
    plot_selection_view._graph_controller.get_visualization = (
        lambda plot_index: (plot, "plot_type") if requested_plots.append(
            plot_index) is None else None
    )

    plot_selection_view._graph_view.display_plot = lambda x, y: "mock_display"

    # Create tabs and clear callback list again
    plot_selection_view._graph_controller.possible_plots_changed_event.publish(
        input_visualizations)
    requested_plots = []

    # Act - mock click of a tab
    plot_selection_view.setCurrentIndex(index_to_click)

    # Assert - check if the correct visualizations are requested (or None if
    #   the plot index was invalid)
    if expected_index_of_plot is None:
        assert requested_plots == []
    else:
        assert requested_plots == [expected_index_of_plot]


@pytest.mark.parametrize("input_visualizations",
                         [
                             ([]),
                             ([PossibleVisualization(0, "str", "s",
                                                     VisGroup.TOPIC, False)]),
                             ([PossibleVisualization(3, "at", "sto",
                                                     VisGroup.CORPUS, True),
                               PossibleVisualization(2, "n2", "2",
                                                     VisGroup.CORPUS, True)]),
                             ([PossibleVisualization(3, "very long name",
                                                     "long name",
                                                     VisGroup.CORPUS, False),
                               PossibleVisualization(5, "", "", VisGroup.MODEL,
                                                     True),
                               PossibleVisualization(7, "1", "2",
                                                     VisGroup.TOPIC, False)])
                         ])
def test_remove_all_tabs(plot: Figure,
                         plot_selection_view: PlotSelectionView,
                         input_visualizations: list[PossibleVisualization]):
    requested_plots = []
    # Mock graph_retrieval from graph_controller and graph view
    plot_selection_view._graph_controller.get_visualization = (
        lambda plot_index: (plot, "plot_type") if requested_plots.append(
            plot_index) is None else None
    )

    plot_selection_view._graph_view.display_plot = lambda x, y: "mock_display"

    # Create tabs and clear callback list again
    plot_selection_view._graph_controller.possible_plots_changed_event.publish(
        input_visualizations)
    requested_plots = []

    # Act - clear all tabs
    plot_selection_view.remove_all_tabs()

    # Assert - check if all tabs are removed and no visualizations were loaded
    assert plot_selection_view.count() == 0
    assert requested_plots == []


@pytest.mark.parametrize("input_visualizations",
                         [
                             ([]),
                             ([PossibleVisualization(0, "str", "s",
                                                     VisGroup.TOPIC, False)]),
                             ([PossibleVisualization(3, "at", "sto",
                                                     VisGroup.CORPUS, True),
                               PossibleVisualization(2, "n2", "2",
                                                     VisGroup.CORPUS, True)]),
                             ([PossibleVisualization(3, "very long name",
                                                     "long name",
                                                     VisGroup.CORPUS, False),
                               PossibleVisualization(5, "", "", VisGroup.MODEL,
                                                     True),
                               PossibleVisualization(7, "1", "2",
                                                     VisGroup.TOPIC, False)])
                         ])
def test_add_spacer_tab(plot: Figure,
                        plot_selection_view: PlotSelectionView,
                        input_visualizations: list[PossibleVisualization],
                        mocker):
    # Define a mock function for get_visualization
    def mock_get_visualization(_):
        return plot, "plot_type"

    # Patch the get_visualization method with the mock
    mocker.patch.object(plot_selection_view._graph_controller,
                        'get_visualization',
                        side_effect=mock_get_visualization)

    plot_selection_view._graph_view.display_plot = lambda x, y: "mock_display"

    # Create tabs and count initial tabs
    plot_selection_view._graph_controller.possible_plots_changed_event.publish(
        input_visualizations)
    initial_count = plot_selection_view.count()

    # Act
    plot_selection_view._add_spacer_tab()

    # Assert - check if one tabs was added and the last tab is disabled
    assert plot_selection_view.count() == initial_count + 1
    assert not plot_selection_view.isTabEnabled(initial_count)


@pytest.mark.parametrize("input_visualizations",
                         [
                             ([]),
                             ([PossibleVisualization(0, "str", "s",
                                                     VisGroup.TOPIC, False)]),
                             ([PossibleVisualization(3, "at", "sto",
                                                     VisGroup.CORPUS, True),
                               PossibleVisualization(2, "n2", "2",
                                                     VisGroup.CORPUS, True)]),
                             ([PossibleVisualization(3, "very long name",
                                                     "long name",
                                                     VisGroup.CORPUS, False),
                               PossibleVisualization(5, "", "", VisGroup.MODEL,
                                                     True),
                               PossibleVisualization(7, "1", "2",
                                                     VisGroup.TOPIC, False)])
                         ])
def test_add_multiple_tabs(plot: Figure,
                           plot_selection_view: PlotSelectionView,
                           input_visualizations: list[PossibleVisualization],
                           mocker):
    # Define a mock function for get_visualization
    def mock_get_visualization(_):
        return plot, "plot_type"

    # Patch the get_visualization method with the mock
    mocker.patch.object(plot_selection_view._graph_controller,
                        'get_visualization',
                        side_effect=mock_get_visualization)

    plot_selection_view._graph_view.display_plot = lambda x, y: "mock_display"

    # Create tabs and count initial tabs
    plot_selection_view._graph_controller.possible_plots_changed_event.publish(
        input_visualizations)
    initial_count = plot_selection_view.count()

    # Act
    plot_selection_view._add_multiple_tabs(input_visualizations)

    # Assert - that the right number of tabs was added
    assert (plot_selection_view.count()
            == initial_count + len(input_visualizations))
    # Assert - that every added tab is correct and enabled
    for (input_index, possible_vis) in enumerate(input_visualizations):
        new_tab_index = initial_count + input_index
        assert plot_selection_view.isTabEnabled(initial_count)
        assert (plot_selection_view.tabText(new_tab_index)
                == possible_vis.short_tab_name)


def test_config_changed_event_no_visualizations(
        plot_selection_view: PlotSelectionView, mocker: MockerFixture):
    # Mock graph_retrieval from graph_controller
    plot_selection_view._graph_controller.visualizations_available = (
        mocker.Mock(return_value=False))
    remove_all_tabs_mock = mocker.patch.object(plot_selection_view,
                                               "remove_all_tabs")
    clear_plot_mock = mocker.patch.object(plot_selection_view._graph_view,
                                          "clear_plot")

    # Act - trigger event
    plot_selection_view._config_changed_event()

    # Assert - check if all tabs are removed and no visualizations were loaded
    remove_all_tabs_mock.assert_called_once()
    clear_plot_mock.assert_called_once()


def test_config_changed_event_with_visualizations(
        plot: Figure,
        plot_selection_view: PlotSelectionView,
        mocker: MockerFixture):
    plot_selection_view._graph_controller.visualizations_available = (
        mocker.Mock(return_value=True))

    # Define a mock function for get_visualization
    def mock_get_visualization(_):
        return plot, "plot_type"

    # Patch the get_visualization method with the mock
    mocker.patch.object(plot_selection_view._graph_controller,
                        'get_visualization',
                        side_effect=mock_get_visualization)

    display_plot_mock = mocker.patch.object(
        plot_selection_view._graph_view,
        "display_plot")

    # Add tabs plots
    plot_selection_view._tabs_plots = {
        0: PossibleVisualization(0, "str", "s", VisGroup.TOPIC, False),
        1: PossibleVisualization(3, "at", "sto", VisGroup.CORPUS, True),
        2: PossibleVisualization(2, "n2", "2", VisGroup.CORPUS, True),
        3: PossibleVisualization(3, "very long name", "long name",
                                 VisGroup.CORPUS, False),
        4: PossibleVisualization(5, "", "", VisGroup.MODEL, True),
        5: PossibleVisualization(7, "1", "2", VisGroup.TOPIC, False)
    }
    plot_selection_view.addTab(QWidget(), "str")
    plot_selection_view.addTab(QWidget(), "at")
    plot_selection_view.addTab(QWidget(), "n2")

    # Set current index to a valid index
    plot_selection_view.setCurrentIndex(0)

    # Act - trigger event
    plot_selection_view._config_changed_event()

    # Assert - check if the visualization is displayed
    display_plot_mock.assert_called_with(plot, "plot_type")


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University
(Department of Information and Computing Sciences)
"""
