import os

import pytest
from PySide6.QtCore import Qt
from PySide6.QtTest import QTest
from PySide6.QtWidgets import QApplication

from tommy.controller.controller import Controller
from tommy.controller.stopwords_controller import StopwordsController
from tommy.controller.synonyms_controller import SynonymsController
from tommy.controller.topic_modelling_controller import \
    TopicModellingController
from tommy.model.stopwords_model import StopwordsModel
from tommy.support.application_settings import application_settings
from tommy.support.supported_languages import SupportedLanguage
from tommy.view.preprocessing_view import PreprocessingView


@pytest.fixture
def app(qtbot):
    """Fixture for setting up the QApplication."""
    _app = QApplication([])
    yield _app
    _app.quit()


@pytest.fixture
def stopwords_controller():
    """Fixture for creating a StopwordsController."""
    return StopwordsController()


@pytest.fixture
def topic_modelling_controller():
    """Fixture for creating a TopicModellingController."""
    return TopicModellingController()


@pytest.fixture
def stopwords_model():
    """Fixture for creating a StopwordsModel."""
    return StopwordsModel()


@pytest.fixture
def synonyms_controller():
    """Fixture for creating a SynonymsController."""
    return SynonymsController()


@pytest.fixture
def preprocessing_view(stopwords_controller,
                       synonyms_controller, topic_modelling_controller):
    """Fixture for creating a StopwordsView."""
    view = PreprocessingView(stopwords_controller,
                             synonyms_controller, topic_modelling_controller)
    return view


def test_stopwords_view_model_linkage(stopwords_controller, preprocessing_view,
                                      stopwords_model, qtbot):
    """Test whether adding stopwords in the view updates the model."""
    # Set up the view and model
    stopwords_controller.set_model_refs(stopwords_model)

    # Add a stopword in the view
    test_stopword = "test_stopword"
    qtbot.keyClicks(preprocessing_view.blacklist_tab, test_stopword)

    # Simulate enter key press to trigger the update
    QTest.keyPress(preprocessing_view.blacklist_tab, Qt.Key_Return)

    # Check if the stopword is added to the model
    assert test_stopword in stopwords_model.extra_words


def test_stopwords_path(stopwords_controller):
    """Test whether the path to the stopwords path is correct depending on
    the language"""
    assert (stopwords_controller.get_stopwords_path(SupportedLanguage.Dutch) ==
            os.path.join(application_settings.data_folder,
                         "preprocessing_data", "stopwords", "Dutch.txt"))
    assert (stopwords_controller.get_stopwords_path(
        SupportedLanguage.English) ==
            os.path.join(application_settings.data_folder,
                         "preprocessing_data", "stopwords", "English.txt"))


def test_stopwords_loaded_on_start():
    controller = Controller()
    loaded_stopwords = (controller.stopwords_controller.stopwords_model
                        .default_words.copy())

    assert len(loaded_stopwords) > 0

    controller.stopwords_controller.load_default_stopwords(
        controller.language_controller.get_language())

    newly_loaded_stopwords = (controller.stopwords_controller.stopwords_model
                              .default_words.copy())

    assert loaded_stopwords == newly_loaded_stopwords


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University
(Department of Information and Computing Sciences)
"""
