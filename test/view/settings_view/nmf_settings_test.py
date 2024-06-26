import pytest

from test.helper_fixtures import controller_no_pipeline
from tommy.view.settings_view.abstract_settings.nmf_settings import NmfSettings


@pytest.fixture
def controller(controller_no_pipeline):
    return controller_no_pipeline


@pytest.fixture(scope='function')
def nmf_settings(controller) -> NmfSettings:
    abstract_settings = NmfSettings(
        controller.model_parameters_controller,
        controller.config_controller,
        controller.language_controller)
    return abstract_settings


@pytest.mark.parametrize("validate_topic_input, validate_word_input",
                         [(True, True), (False, True), (True, False),
                          (False, False)])
def test_all_fields_valid(nmf_settings: NmfSettings,
                          validate_topic_input: bool,
                          validate_word_input: bool,
                          mocker):
    # Mock validate methods
    mocker.patch.object(nmf_settings, "validate_topic_amount_field",
                        return_value=validate_topic_input)
    mocker.patch.object(nmf_settings, "validate_amount_of_words_field",
                        return_value=validate_word_input)

    # Act
    result = nmf_settings.all_fields_valid()

    # Assert
    assert result == (validate_topic_input and
                      validate_word_input)


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University
(Department of Information and Computing Sciences)
"""
