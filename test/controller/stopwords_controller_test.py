import pytest
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication
from PySide6.QtTest import QTest
from tommy.controller.stopwords_controller import StopwordsController
from tommy.controller.synonyms_controller import SynonymsController
from tommy.model.stopwords_model import StopwordsModel
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
def synonyms_controller():
    """Fixture for creating a SynonymsController."""
    return SynonymsController()


@pytest.fixture
def stopwords_model():
    """Fixture for creating a StopwordsModel."""
    return StopwordsModel()


@pytest.fixture
def preprocessing_view(stopwords_controller, synonyms_controller):
    """Fixture for creating a StopwordsView."""
    view = PreprocessingView(stopwords_controller, synonyms_controller)
    return view


def test_stopwords_view_model_linkage(stopwords_controller, preprocessing_view,
                                      stopwords_model, qtbot):
    """Test whether adding stopwords in the view updates the model."""
    stopwords_controller.set_model_refs(stopwords_model)

    # Add a stopword in the view
    test_stopword = "test_stopword"
    qtbot.keyClicks(preprocessing_view.blacklist_tab, test_stopword)

    # Simulate enter key press to trigger the update
    QTest.keyPress(preprocessing_view.blacklist_tab, Qt.Key_Return)

    # Check if the stopword is added to the model
    assert test_stopword in stopwords_model.extra_words
