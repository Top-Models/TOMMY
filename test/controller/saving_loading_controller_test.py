import os

import pytest
from pytestqt.qtbot import QtBot

from tommy.controller.controller import Controller
from tommy.controller.saving_loading_controller import SavingLoadingController
from tommy.model.model import Model
from tommy.support.model_type import ModelType
from tommy.support.supported_languages import SupportedLanguage
from tommy.view.imported_files_view.imported_files_view import \
    ImportedFilesView
from tommy.view.settings_view.abstract_settings.bert_settings import \
    BertSettings
from tommy.view.settings_view.abstract_settings.lda_settings import LdaSettings
from tommy.view.settings_view.abstract_settings.nmf_settings import NmfSettings
from tommy.view.settings_view.model_params_view import ModelParamsView
from tommy.view.stopwords_view import StopwordsView
from test.helper_fixtures import controller_no_pipeline


@pytest.fixture
def controller(controller_no_pipeline) -> Controller:
    return controller_no_pipeline


@pytest.fixture
def saving_loading_controller(controller: Controller) -> (
        SavingLoadingController):
    return controller.saving_loading_controller


@pytest.fixture
def model_params_view(controller: Controller, qtbot: QtBot) -> ModelParamsView:
    model_params_view = ModelParamsView(
        controller.model_parameters_controller,
        controller.language_controller,
        controller.config_controller,
        controller.topic_modelling_controller)
    qtbot.addWidget(model_params_view)
    return model_params_view


@pytest.fixture
def stopwords_view(controller: Controller, qtbot: QtBot) -> StopwordsView:
    stopwords_view = StopwordsView(controller.stopwords_controller)
    qtbot.addWidget(stopwords_view)
    return stopwords_view


@pytest.fixture
def imported_files_view(controller: Controller,
                        qtbot: QtBot) -> ImportedFilesView:
    imported_files_view = (
        ImportedFilesView(controller.corpus_controller,
                          controller.topic_modelling_controller,
                          controller.config_controller))
    qtbot.addWidget(imported_files_view)
    return imported_files_view


def test_load_project(saving_loading_controller: SavingLoadingController,
                      controller: Controller):
    saving_loading_controller.load_settings_from_file(
        "../test/test_data/test_save_files/test load project.json")
    assert (controller.language_controller.get_language() ==
            SupportedLanguage.English)
    assert (controller.config_controller.get_selected_configuration() ==
            "Config 2")

    # check parameters specific to config 2
    assert (controller.model_parameters_controller.get_model_type() ==
            ModelType.NMF)
    assert controller.model_parameters_controller.get_model_n_topics() == 4
    assert controller.model_parameters_controller.get_model_word_amount() == 8
    assert (controller.model_parameters_controller
            .get_model_alpha_beta_custom_enabled() is False)
    assert controller.model_parameters_controller.get_model_alpha() == 1.0
    assert controller.model_parameters_controller.get_model_beta() == 0.01
    assert controller.model_parameters_controller.get_bert_min_df() == 0.1
    assert (controller.model_parameters_controller.get_bert_max_features()
            == 100)
    assert (controller.stopwords_controller.stopwords_model
            .extra_words_in_order == ["misschien"])

    # check parameters specific to config 1
    controller.config_controller.switch_configuration("Config 1")
    assert (controller.model_parameters_controller.get_model_type() ==
            ModelType.LDA)
    assert controller.model_parameters_controller.get_model_n_topics() == 6
    assert controller.model_parameters_controller.get_model_word_amount() == 99
    assert (controller.model_parameters_controller
            .get_model_alpha_beta_custom_enabled() is True)
    assert controller.model_parameters_controller.get_model_alpha() == 13.0
    assert controller.model_parameters_controller.get_model_beta() == 0.02
    assert controller.model_parameters_controller.get_bert_min_df() is None
    assert (controller.model_parameters_controller.get_bert_max_features() is
            None)
    assert (controller.stopwords_controller.stopwords_model
            .extra_words_in_order == ["ja", "tommy"])


def test_save_then_load_project(
        saving_loading_controller: SavingLoadingController,
        controller: Controller):
    # set parameters to some value
    controller.language_controller.set_language(SupportedLanguage.Dutch)
    controller.model_parameters_controller.set_model_type(ModelType.LDA)
    controller.model_parameters_controller.set_model_n_topics(5)
    controller.model_parameters_controller.set_model_word_amount(6)
    (controller.model_parameters_controller
     .set_model_alpha_beta_custom_enabled(True))
    controller.model_parameters_controller.set_model_alpha(2.0)
    controller.model_parameters_controller.set_model_beta(0.2)
    controller.model_parameters_controller.set_bert_min_df(0.1)
    controller.model_parameters_controller.set_bert_max_features(100)
    controller.stopwords_controller.update_stopwords(["hallootjes",
                                                      "goeiedagdag"])

    # add another configuration with different parameters
    controller.config_controller.add_configuration("Andere config")
    controller.model_parameters_controller.set_model_type(ModelType.NMF)
    controller.model_parameters_controller.set_model_n_topics(3)
    controller.model_parameters_controller.set_model_word_amount(4)
    (controller.model_parameters_controller
     .set_model_alpha_beta_custom_enabled(False))
    controller.model_parameters_controller.set_model_alpha(1.0)
    controller.model_parameters_controller.set_model_beta(0.01)
    controller.model_parameters_controller.set_bert_min_df(None)
    controller.model_parameters_controller.set_bert_max_features(None)
    controller.stopwords_controller.update_stopwords(["kan", "niet", "meer"])

    # save parameters
    saving_loading_controller.save_settings_to_file(
        "../test/test_data/test_save_files/test_save_project.json")

    # set parameters to some different value to check if it changes back
    # when loading a configuration
    controller.language_controller.set_language(SupportedLanguage.English)
    controller.model_parameters_controller.set_model_n_topics(7)
    controller.config_controller.add_configuration("Nog een andere config")
    controller.model_parameters_controller.set_model_type(ModelType.LDA)
    controller.model_parameters_controller.set_bert_min_df(0.2)
    controller.stopwords_controller.update_stopwords(["nog", "meer", "woord"])
    controller.config_controller.delete_configuration("Config 1")

    # load the save file that was just created
    saving_loading_controller.load_settings_from_file(
        "../test/test_data/test_save_files/test_save_project.json")

    # check if the parameters are set to the values that were saved
    assert (controller.language_controller.get_language() ==
            SupportedLanguage.Dutch)
    assert (controller.config_controller.get_selected_configuration() ==
            "Andere config")
    assert (controller.model_parameters_controller.get_model_type() ==
            ModelType.NMF)
    assert controller.model_parameters_controller.get_model_n_topics() == 3
    assert controller.model_parameters_controller.get_model_word_amount() == 4
    assert (controller.model_parameters_controller
            .get_model_alpha_beta_custom_enabled() is False)
    assert controller.model_parameters_controller.get_model_alpha() == 1.0
    assert controller.model_parameters_controller.get_model_beta() == 0.01
    assert controller.model_parameters_controller.get_bert_min_df() is None
    assert (controller.model_parameters_controller.get_bert_max_features() is
            None)
    assert (controller.stopwords_controller.stopwords_model
            .extra_words_in_order == ["kan", "niet", "meer"])

    # check if the other configuration was also saved correctly
    controller.config_controller.switch_configuration("Config 1")
    assert (controller.model_parameters_controller.get_model_type() ==
            ModelType.LDA)
    assert controller.model_parameters_controller.get_model_n_topics() == 5
    assert controller.model_parameters_controller.get_model_word_amount() == 6
    assert (controller.model_parameters_controller
            .get_model_alpha_beta_custom_enabled() is True)
    assert controller.model_parameters_controller.get_model_alpha() == 2.0
    assert controller.model_parameters_controller.get_model_beta() == 0.2
    assert controller.model_parameters_controller.get_bert_min_df() == 0.1
    assert (controller.model_parameters_controller.get_bert_max_features() ==
            100)
    assert (controller.stopwords_controller.stopwords_model
            .extra_words_in_order == ["hallootjes", "goeiedagdag"])


def test_load_project_updates_parameter_view(
        model_params_view: ModelParamsView,
        controller: Controller):
    # load test project
    controller.saving_loading_controller.load_settings_from_file(
        "../test/test_data/test_save_files/test load project.json")

    # check if the correct AbstractSettings view is shown
    nmf_settings_view: NmfSettings = (
        model_params_view.algorithm_specific_settings_views)[
        ModelType.NMF]
    assert model_params_view.get_current_settings_view() is nmf_settings_view

    # check if the fields are updated correctly
    assert nmf_settings_view._topic_amount_field.text() == "4"
    assert nmf_settings_view._amount_of_words_field.text() == "8"
    assert nmf_settings_view._algorithm_field.currentText() == "NMF"
    assert nmf_settings_view._language_field.currentText() == "Engels"

    # switch to config 1
    controller.config_controller.switch_configuration("Config 1")

    # check if the correct AbstractSettings view is shown
    lda_settings_view: LdaSettings = (
        model_params_view.algorithm_specific_settings_views)[
        ModelType.LDA]
    assert model_params_view.get_current_settings_view() is lda_settings_view

    # check if the fields are updated correctly
    assert lda_settings_view._topic_amount_field.text() == "6"
    assert lda_settings_view._amount_of_words_field.text() == "99"
    assert lda_settings_view._algorithm_field.currentText() == "LDA"
    assert lda_settings_view._language_field.currentText() == "Engels"
    assert (lda_settings_view._auto_calc_alpha_beta_checkbox.isChecked() is
            False)
    assert lda_settings_view._alpha_value_input.text() == "13.0"
    assert lda_settings_view._beta_value_input.text() == "0.02"


def test_load_project_updates_bert_parameter_view(
        model_params_view: ModelParamsView,
        controller: Controller):
    # load bert test project
    controller.saving_loading_controller.load_settings_from_file(
        "../test/test_data/test_save_files/test load bert project.json")

    # check if correct settings view is loaded
    bert_settings_view: BertSettings = (
        model_params_view.algorithm_specific_settings_views)[
        ModelType.BERTopic]
    assert model_params_view.get_current_settings_view() is bert_settings_view

    # check if the fields are updated correctly
    assert bert_settings_view._min_df_input.text() == "0.1"
    assert bert_settings_view._max_features_input.text() == "100"


def test_load_project_updates_bert_parameter_view_when_none(
        model_params_view: ModelParamsView,
        controller: Controller):
    # load bert test project
    controller.saving_loading_controller.load_settings_from_file(
        "../test/test_data/test_save_files/test load bert project none "
        "parameters.json")

    # check if correct settings view is loaded
    bert_settings_view: BertSettings = (
        model_params_view.algorithm_specific_settings_views)[
        ModelType.BERTopic]
    assert model_params_view.get_current_settings_view() is bert_settings_view

    # check that input field is empty, because the value is None
    assert bert_settings_view._min_df_input.text() == ""
    assert bert_settings_view._max_features_input.text() == ""


def test_load_project_updates_stopwords_view(
        stopwords_view: StopwordsView,
        controller: Controller):
    # load test project
    controller.saving_loading_controller.load_settings_from_file(
        "../test/test_data/test_save_files/test load project.json")

    # check if the stopwords are updated correctly
    assert stopwords_view.blacklist_tab.toPlainText() == "misschien"

    # switch to config 1
    controller.config_controller.switch_configuration("Config 1")

    # check if the stopwords are updated correctly
    assert stopwords_view.blacklist_tab.toPlainText() == "ja\ntommy"


def test_load_project_imports_files(controller: Controller):
    # load test project
    controller.saving_loading_controller.load_settings_from_file(
        "../test/test_data/test_save_files/test load project.json")

    # check if the files are imported correctly
    metadata = controller.corpus_controller._corpus_model.metadata
    assert len(metadata) == 2
    file_names = [metadata[i].name for i in range(2)]
    assert sorted(file_names) == ["kattenverhaaltje 1",
                                  "kattenverhaaltje 2"]


def test_load_project_updates_imported_files_view(
        imported_files_view: ImportedFilesView,
        controller: Controller):
    # load test project
    controller.saving_loading_controller.load_settings_from_file(
        "../test/test_data/test_save_files/test load project.json")

    # get metadata from corpus model
    metadata = controller.corpus_controller._corpus_model.metadata

    # check if the file_container contains the correct metadata
    files_view_metadata = imported_files_view.metadata
    assert len(files_view_metadata) == 2
    assert files_view_metadata == metadata

    # check if the files are displayed correctly
    assert imported_files_view.scroll_layout.count() == 2
    scroll_layout_filenames = [imported_files_view.scroll_layout.itemAt(i)
                               .widget().text() for i in range(2)]
    assert sorted(scroll_layout_filenames) == ["kattenverhaaltje 1",
                                               "kattenverhaaltje 2"]


def test_loading_invalid_project_files(
        saving_loading_controller: SavingLoadingController):
    """
    Test if the loading of invalid files returns False
    Files are invalid if they are not json files, if they do not contain all
    necessary fields or if they contain invalid values
    :param saving_loading_controller:
    :return:
    """
    folder_path = "../test/test_data/test_save_files/invalid_save_files"
    # load all files from a folder
    files = os.listdir(folder_path)
    for file in files:
        assert saving_loading_controller.load_settings_from_file(
            os.path.join(folder_path, file)) != []
