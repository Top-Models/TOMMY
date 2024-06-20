import pytest
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication
from PySide6.QtTest import QTest

from tommy.controller.language_controller import LanguageController
from tommy.model.language_model import LanguageModel
from pytest_mock import mocker

from tommy.support.supported_languages import SupportedLanguage


@pytest.fixture
def language_controller():
    language_controller = LanguageController()
    language_model = LanguageModel()
    language_controller.set_model_refs(language_model)
    return language_controller


def test_change_language_event(language_controller, mocker: mocker):
    """Test whether the change_language_event gets updated every time the
    language gets changed"""
    change_language_event = mocker.patch.object(
        language_controller.change_language_event, 'publish')
    language_controller.set_language(SupportedLanguage.Dutch)
    assert change_language_event.call_count == 1
    language_controller.set_language(SupportedLanguage.English)
    assert change_language_event.call_count == 2
    language_controller.set_language(SupportedLanguage.Dutch)
    assert change_language_event.call_count == 3


def test_update_language(language_controller):
    """Test whether the get_language and set_language correctly update the
    language model and return the correct values"""
    language_controller.set_language(SupportedLanguage.Dutch)
    assert language_controller.get_language() == SupportedLanguage.Dutch
    language_controller.set_language(SupportedLanguage.English)
    assert language_controller.get_language() == SupportedLanguage.English

"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University
(Department of Information and Computing Sciences)
"""
