import pytest
from PySide6.QtWidgets import QWidget
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


def test_get_active_tab_name(plot_selection_view: PlotSelectionView):
    """
    Test getting the name of the active tab.
    """

    # Arrange
    plot_selection_view.removeTab(0)
    plot_selection_view.removeTab(0)
    plot_selection_view.addTab(QWidget(), "lda_model")
    plot_selection_view.addTab(QWidget(), "nmf_model")

    # Act & Assert
    assert plot_selection_view.get_active_tab_name() == "lda_model"
    plot_selection_view.setCurrentIndex(1)
    assert plot_selection_view.get_active_tab_name() == "nmf_model"


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University 
(Department of Information and Computing Sciences)
"""