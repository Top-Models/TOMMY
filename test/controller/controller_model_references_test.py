import pytest
from pytest_mock import MockerFixture

from test.helper_fixtures import controller_no_pipeline
from tommy.controller.controller import Controller


@pytest.fixture
def controller(controller_no_pipeline):
    return controller_no_pipeline


def test_controller_refs(controller: Controller):
    # Get all controller submodules from Controller
    model_parameters_controller = controller.model_parameters_controller
    language_controller = controller.language_controller
    graph_controller = controller.graph_controller
    topic_modelling_controller = controller.topic_modelling_controller
    stopwords_controller = controller.stopwords_controller
    synonyms_controller = controller.synonyms_controller
    preprocessing_controller = controller.preprocessing_controller
    corpus_controller = controller.corpus_controller
    project_settings_controller = controller.project_settings_controller
    saving_loading_controller = controller.saving_loading_controller
    config_controller = controller.config_controller
    export_controller = controller.export_controller

    # Check if all controllers have the correct references to each other

    assert graph_controller._corpus_controller is corpus_controller
    # the GraphController.set_controller_refs method also takes a
    # TopicModellingController and ProjectSettingsController as input,
    # but those are only used for subscribing to events, so they are not
    # stored in the GraphController

    assert topic_modelling_controller._model_parameters_controller is (
        model_parameters_controller)
    assert topic_modelling_controller._corpus_controller is corpus_controller
    assert (topic_modelling_controller._stopwords_controller is
            stopwords_controller)
    assert (topic_modelling_controller._synonyms_controller is
            synonyms_controller)
    assert topic_modelling_controller._preprocessing_controller is (
        preprocessing_controller)

    assert stopwords_controller._language_controller is language_controller

    assert preprocessing_controller._language_controller is language_controller

    assert corpus_controller._project_settings_controller is (
        project_settings_controller)
    assert corpus_controller._preprocessing_controller is (
        preprocessing_controller)

    assert config_controller._graph_controller is graph_controller

    assert export_controller._graph_controller is graph_controller
    assert export_controller._topic_modelling_controller is (
        topic_modelling_controller)


def test_model_refs(controller: Controller):
    helper_check_model_refs(controller)


def helper_check_model_refs(controller: Controller):
    # Get all controller sub-modules from Controller
    model_parameters_controller = controller.model_parameters_controller
    language_controller = controller.language_controller
    graph_controller = controller.graph_controller
    topic_modelling_controller = controller.topic_modelling_controller
    stopwords_controller = controller.stopwords_controller
    synonyms_controller = controller.synonyms_controller
    preprocessing_controller = controller.preprocessing_controller
    corpus_controller = controller.corpus_controller
    project_settings_controller = controller.project_settings_controller
    saving_loading_controller = controller.saving_loading_controller
    config_controller = controller.config_controller
    export_controller = controller.export_controller

    # Get all model submodules of the current configuration
    model = controller._model
    config_model = model.config_model
    corpus_model = model.corpus_model
    topic_name_model = model.topic_name_model
    language_model = model.language_model
    model_parameters_model = model.model_parameters_model
    project_settings_model = model.project_settings_model
    stopwords_model = model.stopwords_model
    synonyms_model = model.synonyms_model
    topic_model = model.topic_model

    assert (project_settings_controller._project_settings_model is
            project_settings_model)

    assert config_controller._model is model

    assert (model_parameters_controller._model_parameters_model is
            model_parameters_model)

    assert topic_modelling_controller._topic_model is topic_model
    assert topic_modelling_controller._config_model is config_model

    assert stopwords_controller._stopwords_model is stopwords_model

    assert synonyms_controller._synonyms_model is synonyms_model

    assert preprocessing_controller._stopwords_model is stopwords_model
    assert preprocessing_controller._synonyms_model is synonyms_model

    assert corpus_controller._corpus_model is corpus_model

    assert (project_settings_controller._project_settings_model is
            project_settings_model)
    assert language_controller._language_model is language_model
    assert saving_loading_controller._model is model
    assert graph_controller._topic_name_model is topic_name_model


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University
(Department of Information and Computing Sciences)
"""
