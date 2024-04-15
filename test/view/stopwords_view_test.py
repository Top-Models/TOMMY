import pytest
from PySide6.QtCore import Qt
from pytestqt.qtbot import QtBot

from tommy.controller.controller import Controller
from tommy.support.constant_variables import sec_col_purple, text_font
from tommy.view.model_params_view import ModelParamsView
from tommy.view.stopwords_view import StopwordsView


@pytest.fixture(scope='function')
def stopwords_view(qtbot: QtBot) -> StopwordsView:
    controller = Controller()
    stopwords_view = StopwordsView(controller.stopwords_controller)
    qtbot.addWidget(stopwords_view)
    return stopwords_view


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University 
(Department of Information and Computing Sciences)
"""
