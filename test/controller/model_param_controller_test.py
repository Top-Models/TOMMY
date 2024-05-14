import pytest
from tommy.controller.model_parameters_controller import (
    ModelParametersController)
from tommy.model.model_parameters_model import ModelParametersModel
from tommy.support.model_type import ModelType


@pytest.fixture(scope='function')
def model_parameters_controller() -> ModelParametersController:
    controller = ModelParametersController()
    model = ModelParametersModel()
    controller.set_model_refs(model)
    return controller


def test_init(model_parameters_controller: ModelParametersController):
    assert model_parameters_controller._parameters_model is not None
    assert model_parameters_controller._algorithm_changed_event is not None


def test_set_model_refs(
        model_parameters_controller: ModelParametersController):
    model = ModelParametersModel()
    model_parameters_controller.set_model_refs(model)
    assert model_parameters_controller._parameters_model == model


def test_set_get_model_word_amount(
        model_parameters_controller: ModelParametersController):
    model_parameters_controller.set_model_word_amount(10)
    assert model_parameters_controller.get_model_word_amount() == 10


def test_set_get_model_alpha_beta_custom_enabled(
        model_parameters_controller: ModelParametersController):
    model_parameters_controller.set_model_alpha_beta_custom_enabled(True)
    assert (model_parameters_controller.get_model_alpha_beta_custom_enabled()
            is True)


def test_set_get_model_alpha(
        model_parameters_controller: ModelParametersController):
    model_parameters_controller.set_model_alpha(0.5)
    assert model_parameters_controller.get_model_alpha() == 0.5


def test_set_get_model_beta(
        model_parameters_controller: ModelParametersController):
    model_parameters_controller.set_model_beta(0.5)
    assert model_parameters_controller.get_model_beta() == 0.5


def test_set_get_model_n_topics(
        model_parameters_controller: ModelParametersController):
    model_parameters_controller.set_model_n_topics(5)
    assert model_parameters_controller.get_model_n_topics() == 5


def test_set_get_model_type(
        model_parameters_controller: ModelParametersController):
    model_parameters_controller.set_model_type(ModelType.NMF)
    assert model_parameters_controller.get_model_type() == ModelType.NMF
