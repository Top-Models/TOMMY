import pytest
from pytest_mock import MockerFixture

from test.helper_fixtures import controller_no_pipeline
from tommy.controller.controller import Controller


@pytest.fixture
def controller(controller_no_pipeline):
    return controller_no_pipeline


def test_controller_refs(controller: Controller):
    model_parameter_controller = controller.model_parameters_controller
    graph_controller = controller.graph_controller
    topic_modelling_controller = controller._topic_modelling_controller
    stopwords_controller = controller.stopwords_controller
    preprocessing_controller = controller._preprocessing_controller
    corpus_controller = controller.corpus_controller
    project_settings_controller = controller.project_settings_controller
    config_controller = controller.config_controller
    saving_loading_controller = controller.saving_loading_controller

    assert (corpus_controller._project_settings_controller is
            project_settings_controller)

    assert (graph_controller._topic_modelling_controller is
            topic_modelling_controller)

    assert (graph_controller._corpus_controller is
            corpus_controller)

    assert (topic_modelling_controller._model_parameters_controller is
            model_parameter_controller)

    assert (topic_modelling_controller._corpus_controller is
            corpus_controller)


def test_model_refs(controller: Controller):
    helper_check_model_refs(controller)


def helper_check_model_refs(controller: Controller):
    model_parameter_controller = controller.model_parameters_controller
    graph_controller = controller.graph_controller
    topic_modelling_controller = controller._topic_modelling_controller
    stopwords_controller = controller.stopwords_controller
    preprocessing_controller = controller._preprocessing_controller
    corpus_controller = controller.corpus_controller
    project_settings_controller = controller.project_settings_controller
    config_controller = controller.config_controller
    saving_loading_controller = controller.saving_loading_controller

    model = controller._model
    corpus_model = model.corpus_model
    model_parameters_model = model.model_parameters_model
    project_settings_model = model.project_settings_model
    stopwords_model = model.stopwords_model
    topic_model = model.topic_model

    assert (project_settings_controller._project_settings_model is
            project_settings_model)

    assert config_controller._model is model

    assert (model_parameter_controller._parameters_model is
            model_parameters_model)

    assert (topic_modelling_controller._topic_model is
            topic_model)

    assert (stopwords_controller._stopwords_model is
            stopwords_model)

    assert (preprocessing_controller._stopwords_model is
            stopwords_model)

    assert corpus_controller._corpus_model is corpus_model

    assert saving_loading_controller._model is model


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University
(Department of Information and Computing Sciences)
"""
