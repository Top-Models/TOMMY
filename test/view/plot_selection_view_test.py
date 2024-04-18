import pytest
from pytestqt.qtbot import QtBot

from tommy.controller.controller import Controller
from tommy.view.plot_selection_view import PlotSelectionView


@pytest.fixture(scope='function')
def plot_selection_view(qtbot: QtBot) -> PlotSelectionView:
    controller = Controller()
    plot_selection_view = PlotSelectionView(
        controller.graph_controller
    )
    qtbot.addWidget(plot_selection_view)
    return plot_selection_view


def test_get_active_tab_name(plot_selection_view: PlotSelectionView, mocker):
    """
    Test getting the name of the active tab.
    """
    # Arrange
    plot_selection_view.setCurrentIndex(0)
    plot_selection_view.setTabVisible(4, True)
    plot_selection_view.setTabVisible(5, True)

    # Mock update_current_visualization method of the graph controller
    plot_selection_view._graph_controller.update_current_visualization = \
        lambda x: True

    # Act & Assert
    assert plot_selection_view.get_active_tab_name() == "Correlatie"
    plot_selection_view.setCurrentIndex(1)
    assert plot_selection_view.get_active_tab_name() == "Topic Netwerk"
    plot_selection_view.setCurrentIndex(2)
    assert plot_selection_view.get_active_tab_name() == "Doc. Netwerk"
    plot_selection_view.setCurrentIndex(3)
    assert plot_selection_view.get_active_tab_name() == "Woordaantal"
    plot_selection_view.setCurrentIndex(4)
    assert plot_selection_view.get_active_tab_name() == "Woordenwolk"
    plot_selection_view.setCurrentIndex(5)
    assert plot_selection_view.get_active_tab_name() == "Woordgewichten"


def test_tab_clicked_event(plot_selection_view: PlotSelectionView):
    # Mock update_current_visualization method of the graph controller
    plot_selection_view._graph_controller.update_current_visualization = \
        lambda x: True

    # Act
    plot_selection_view.tab_clicked_event()

    # Assert
    assert plot_selection_view._graph_controller._current_tab_index == 0


def test_toggle_topic_specific_tabs_visible(
        plot_selection_view: PlotSelectionView):
    # Act
    plot_selection_view.toggle_topic_specific_tabs(True)

    # Assert
    assert plot_selection_view.isTabVisible(4)
    assert plot_selection_view.isTabVisible(5)


def test_toggle_topic_specific_tabs_invisible(
        plot_selection_view: PlotSelectionView):
    # Act
    plot_selection_view.toggle_topic_specific_tabs(False)

    # Assert
    assert not plot_selection_view.isTabVisible(4)
    assert not plot_selection_view.isTabVisible(5)


@pytest.mark.parametrize("visible, current_tab_index, expected_tab_index", [
    (True, 0, 0),
    (False, 0, 0),
    (True, 1, 1),
    (False, 1, 1),
    (True, 2, 2),
    (False, 2, 2),
    (True, 3, 3),
    (False, 3, 3),
    (False, 4, 0),
    (False, 5, 0)
])
def test_toggle_topic_specific_tabs_current_index(
        plot_selection_view: PlotSelectionView,
        visible: bool,
        current_tab_index: int,
        expected_tab_index: int):
    # Arrange
    plot_selection_view.tab_clicked_event = lambda: True
    plot_selection_view.setCurrentIndex(current_tab_index)

    # Act
    plot_selection_view.toggle_topic_specific_tabs(visible)

    # Assert
    assert plot_selection_view.currentIndex() == expected_tab_index


def test_update_observer(plot_selection_view: PlotSelectionView):
    # Mock the get topic amount method of the graph controller
    plot_selection_view._graph_controller.get_number_of_topics = lambda: 5

    # Act
    plot_selection_view.update_observer(None)

    # Assert
    assert plot_selection_view._graph_controller._current_tab_index == 0


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University 
(Department of Information and Computing Sciences)
"""
