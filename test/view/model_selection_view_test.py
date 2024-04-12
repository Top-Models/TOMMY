import pytest
from PySide6.QtWidgets import QWidget
from pytestqt.qtbot import QtBot

from tommy.view.model_selection_view import ModelSelectionView


@pytest.fixture(scope='function')
def model_selection_view(qtbot: QtBot) -> ModelSelectionView:
    model_selection_view = ModelSelectionView()
    qtbot.addWidget(model_selection_view)
    return model_selection_view


def test_get_active_tab_name(model_selection_view: ModelSelectionView):
    """
    Test getting the name of the active tab.
    """

    # Arrange
    model_selection_view.removeTab(0)
    model_selection_view.removeTab(0)
    model_selection_view.addTab(QWidget(), "lda_model")
    model_selection_view.addTab(QWidget(), "nmf_model")

    # Act & Assert
    assert model_selection_view.get_active_tab_name() == "lda_model"
    model_selection_view.setCurrentIndex(1)
    assert model_selection_view.get_active_tab_name() == "nmf_model"

