import os

import pytest
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication
from PySide6.QtTest import QTest

from tommy.controller.language_controller import LanguageController
from tommy.controller.stopwords_controller import StopwordsController
from tommy.model.language_model import LanguageModel
from tommy.model.stopwords_model import StopwordsModel
from tommy.support.application_settings import application_settings
from tommy.support.supported_languages import SupportedLanguage
from tommy.view.stopwords_view import StopwordsView


@pytest.fixture
def app(qtbot):
    """Fixture for setting up the QApplication."""
    _app = QApplication([])
    yield _app
    _app.quit()


@pytest.fixture
def language_controller():
    """Fixture for creating a LanguageController."""
    language_controller = LanguageController()
    language_controller.set_model_refs(LanguageModel())
    return language_controller


@pytest.fixture
def stopwords_controller(language_controller):
    """Fixture for creating a StopwordsController."""
    return StopwordsController(language_controller)


@pytest.fixture
def stopwords_model():
    """Fixture for creating a StopwordsModel."""
    return StopwordsModel()


@pytest.fixture
def stopwords_view(stopwords_controller):
    """Fixture for creating a StopwordsView."""
    view = StopwordsView(stopwords_controller)
    return view


def test_stopwords_view_model_linkage(stopwords_controller, stopwords_view,
                                      stopwords_model, qtbot):
    """Test whether adding stopwords in the view updates the model."""
    # Set up the view and model
    stopwords_view.show()
    stopwords_controller.set_model_refs(stopwords_model)

    # Add a stopword in the view
    test_stopword = "test_stopword"
    qtbot.keyClicks(stopwords_view.blacklist_tab, test_stopword)

    # Simulate enter key press to trigger the update
    QTest.keyPress(stopwords_view.blacklist_tab, Qt.Key_Return)

    # Check if the stopword is added to the model
    assert test_stopword in stopwords_model.extra_words


def test_stopwords_path(stopwords_controller, language_controller):
    """Test whether the path to the stopwords path is correct depending on
    the language"""
    assert (stopwords_controller.get_stopwords_path(SupportedLanguage.Dutch) ==
            os.path.join(application_settings.preprocessing_data_folder,
                         "stopwords", "Dutch.txt"))
    assert (stopwords_controller.get_stopwords_path(
        SupportedLanguage.English) ==
            os.path.join(application_settings.preprocessing_data_folder,
                         "stopwords", "English.txt"))
