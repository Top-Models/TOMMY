import pytest
from pytest_mock import MockerFixture
from pytestqt.qtbot import QtBot

from tommy.controller.config_controller import ConfigController
from tommy.controller.controller import Controller
from tommy.controller.language_controller import LanguageController
from tommy.controller.model_parameters_controller import \
    ModelParametersController
from tommy.controller.stopwords_controller import StopwordsController
from tommy.controller.topic_modelling_controller import \
    TopicModellingController
from tommy.support.model_type import ModelType
from tommy.view.settings_view.abstract_settings.lda_settings import LdaSettings
from tommy.view.settings_view.model_params_view import ModelParamsView
from tommy.view.stopwords_view import StopwordsView
from test.helper_fixtures import controller_no_pipeline


@pytest.fixture
def controller(controller_no_pipeline):
    return controller_no_pipeline


@pytest.fixture
def config_controller(controller: Controller) -> ConfigController:
    return controller.config_controller


@pytest.fixture
def model_parameters_controller(controller: Controller) -> (
        ModelParametersController):
    return controller.model_parameters_controller


@pytest.fixture
def language_controller(controller: Controller) -> LanguageController:
    return controller.language_controller


@pytest.fixture
def topic_modelling_controller(
        controller: Controller) -> TopicModellingController:
    return controller.topic_modelling_controller


@pytest.fixture
def model_params_view(controller: Controller,
                      model_parameters_controller: ModelParametersController,
                      config_controller: ConfigController,
                      language_controller: LanguageController,
                      topic_modelling_controller: TopicModellingController,
                      qtbot: QtBot) -> ModelParamsView:
    model_params_view = ModelParamsView(model_parameters_controller,
                                        language_controller,
                                        config_controller,
                                        topic_modelling_controller)
    qtbot.addWidget(model_params_view)
    return model_params_view


# stopwords controller fixture
@pytest.fixture
def stopwords_controller(controller: Controller) -> StopwordsController:
    return controller.stopwords_controller


@pytest.fixture
def stopwords_view(stopwords_controller: StopwordsController) -> StopwordsView:
    return StopwordsView(stopwords_controller)


def test_config_updates_lda_num_topics_textbox(
        model_params_view: ModelParamsView,
        config_controller: ConfigController):
    # get reference to textbox for amount of topics
    lda_settings_view = model_params_view.algorithm_specific_settings_views[
        ModelType.LDA]

    num_topics = 6

    # add configuration "6 topics" and set topic amount to 6
    config_controller.add_configuration("6 topics")
    lda_settings_view._topic_amount_field.setText(str(num_topics))
    lda_settings_view._topic_amount_field.editingFinished.emit()

    # add configuration "5 topics" and set topic amount to 5
    config_controller.add_configuration("5 topics")
    lda_settings_view._topic_amount_field.setText(str(5))
    lda_settings_view._topic_amount_field.editingFinished.emit()

    # switch to config "6 topics"
    config_controller.switch_configuration("6 topics")

    # assert that get_topic_amount returns 6
    assert lda_settings_view.get_topic_amount() == num_topics


def test_config_updates_lda_amount_of_words_textbox(
        model_params_view: ModelParamsView,
        config_controller: ConfigController):
    # get reference to textbox for amount of words
    lda_settings_view = model_params_view.algorithm_specific_settings_views[
        ModelType.LDA]

    num_words = 6

    # add configuration "6 words" and set amount of words to 6
    config_controller.add_configuration("6 words")
    lda_settings_view._amount_of_words_field.setText(str(num_words))
    lda_settings_view._amount_of_words_field.editingFinished.emit()

    # add configuration "5 words" and set amount of words to 5
    config_controller.add_configuration("5 words")
    lda_settings_view._amount_of_words_field.setText(str(5))
    lda_settings_view._amount_of_words_field.editingFinished.emit()

    # switch to config "6 words"
    config_controller.switch_configuration("6 words")

    # assert that get_topic_amount returns 6
    assert lda_settings_view.get_amount_of_words() == num_words


def test_config_updates_lda_alpha_value_textbox(
        model_params_view: ModelParamsView,
        config_controller: ConfigController,
        model_parameters_controller: ModelParametersController):
    # get reference to textbox for alpha value
    lda_settings_view: LdaSettings = (
        model_params_view.algorithm_specific_settings_views)[
        ModelType.LDA]

    alpha_value = 0.5

    # add configuration "0.5 alpha value" and set alpha value to 0.5
    config_controller.add_configuration("0.5 alpha value")
    lda_settings_view._auto_calc_alpha_beta_checkbox.setChecked(False)
    lda_settings_view._alpha_value_input.setText(str(alpha_value))
    lda_settings_view._alpha_value_input.editingFinished.emit()

    # add configuration "0.6 alpha value" and set alpha value to 0.6
    config_controller.add_configuration("0.6 alpha value")
    lda_settings_view._alpha_value_input.setText(str(0.6))
    lda_settings_view._alpha_value_input.editingFinished.emit()

    # switch to config "0.5 alpha value"
    config_controller.switch_configuration("0.5 alpha value")

    # assert that get_alpha_value returns 0.5
    assert lda_settings_view._alpha_value_input.text() == str(alpha_value)


def test_config_updates_lda_beta_value_textbox(
        model_params_view: ModelParamsView,
        config_controller: ConfigController,
        model_parameters_controller: ModelParametersController):
    # get reference to textbox for beta value
    lda_settings_view: LdaSettings = (
        model_params_view.algorithm_specific_settings_views)[
        ModelType.LDA]

    beta_value = 0.5

    # add configuration "0.5 beta value" and set beta value to 0.5
    config_controller.add_configuration("0.5 beta value")
    lda_settings_view._auto_calc_alpha_beta_checkbox.setChecked(False)
    lda_settings_view._beta_value_input.setText(str(beta_value))
    lda_settings_view._beta_value_input.editingFinished.emit()

    # add configuration "0.6 beta value" and set beta value to 0.6
    config_controller.add_configuration("0.6 beta value")
    lda_settings_view._beta_value_input.setText(str(0.6))
    lda_settings_view._beta_value_input.editingFinished.emit()

    # switch to config "0.5 beta value"
    config_controller.switch_configuration("0.5 beta value")

    # assert that get_beta_value returns 0.5
    assert lda_settings_view._beta_value_input.text() == str(beta_value)


def test_config_updates_lda_alpha_beta_checkbox(
        model_params_view: ModelParamsView,
        config_controller: ConfigController,
        model_parameters_controller: ModelParametersController):
    # get reference to checkbox for auto calculating alpha and beta
    lda_settings_view: LdaSettings = (
        model_params_view.algorithm_specific_settings_views)[
        ModelType.LDA]

    # add configuration "auto calc alpha beta" and set checkbox to checked
    config_controller.add_configuration("auto calc alpha beta")
    lda_settings_view._auto_calc_alpha_beta_checkbox.setChecked(True)

    # add configuration "manual alpha beta" and set checkbox to unchecked
    config_controller.add_configuration("manual alpha beta")
    lda_settings_view._auto_calc_alpha_beta_checkbox.setChecked(False)

    # switch to config "auto calc alpha beta"
    config_controller.switch_configuration("auto calc alpha beta")

    # assert that auto_calc_alpha_beta_checkbox is checked
    assert lda_settings_view._auto_calc_alpha_beta_checkbox.isChecked() is True

    # switch to config "manual alpha beta"
    config_controller.switch_configuration("manual alpha beta")

    # assert that auto_calc_alpha_beta_checkbox is unchecked
    assert (lda_settings_view._auto_calc_alpha_beta_checkbox.isChecked() is
            False)


def test_config_updates_algorithm_dropdown(
        model_params_view: ModelParamsView,
        config_controller: ConfigController):
    # add configuration "NMF" and set algorithm to "NMF"
    config_controller.add_configuration("NMF")
    settings_view = model_params_view.get_current_settings_view()
    settings_view._algorithm_field.setCurrentText("NMF")

    # add configuration "LDA" and set algorithm to "LDA"
    config_controller.add_configuration("LDA")
    settings_view = model_params_view.get_current_settings_view()
    settings_view._algorithm_field.setCurrentText("LDA")

    # switch to config "NMF"
    config_controller.switch_configuration("NMF")
    settings_view = model_params_view.get_current_settings_view()

    # assert that algorithm_field is set to "NMF"
    assert settings_view._algorithm_field.currentText() == "NMF"


def test_config_updates_blacklist_textbox(
        stopwords_view: StopwordsView,
        config_controller: ConfigController):
    # get reference to textbox for blacklist
    blacklist_tab = stopwords_view.blacklist_tab

    test_words = "word5\nword1\nword2"

    # add configuration "blacklist" and set blacklist to "word1 word2"
    config_controller.add_configuration("blacklist")
    blacklist_tab.setText(test_words)

    # add configuration "blacklist2" and set blacklist to "word3 word4"
    config_controller.add_configuration("blacklist2")
    blacklist_tab.setText("word3\nword4")

    # switch to config "blacklist"
    config_controller.switch_configuration("blacklist")

    # assert that blacklist_tab text is test_words
    assert blacklist_tab.toPlainText() == test_words

# TODO: implement and then test the behaviour for the other tabs in the
#  stopwords view


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University
(Department of Information and Computing Sciences)
"""