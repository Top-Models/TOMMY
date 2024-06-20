import pytest
from pytestqt.qtbot import QtBot

from tommy.controller.controller import Controller
from tommy.view.preprocessing_view import PreprocessingView


@pytest.fixture(scope='function')
def preprocessing_view(qtbot: QtBot) -> PreprocessingView:
    controller = Controller()
    preprocessing_view = PreprocessingView(controller.stopwords_controller,
                                           controller.synonyms_controller)
    qtbot.addWidget(preprocessing_view)
    return preprocessing_view


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University
(Department of Information and Computing Sciences)
"""
