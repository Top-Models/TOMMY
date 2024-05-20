from unittest.mock import Mock

import pytest
from pytest_mock import MockerFixture

from test.controller.controller_model_references_test import (
    helper_check_model_refs)
from tommy.controller.config_controller import ConfigController
from tommy.controller.controller import Controller


@pytest.fixture
def controller():
    return Controller()


@pytest.fixture
def config_controller(controller: Controller):
    return controller.config_controller


def test_model_references_after_add_config(
        controller: Controller, config_controller: ConfigController):
    # add a configuration (and implicitly switch to it)
    config_controller.add_configuration("Config 2")

    # use helper function which asserts that all controllers point to the
    # models of the current configuration
    helper_check_model_refs(controller)


def test_model_references_after_switch_config(
        controller: Controller, config_controller: ConfigController):
    # add two configurations
    config_controller.add_configuration("Config 2")
    config_controller.add_configuration("Config 3")

    # switch back to config 2
    config_controller.switch_configuration("Config 2")

    # use helper function which asserts that all controllers point to the
    # models of the current configuration
    helper_check_model_refs(controller)


def test_config_add(config_controller: ConfigController):
    add_success1 = config_controller.add_configuration("Config 2")
    add_success2 = config_controller.add_configuration("Config 3")

    config_names = config_controller.get_configuration_names()

    assert "Config 2" in config_names
    assert "Config 3" in config_names

    assert add_success1 is True
    assert add_success2 is True

    assert config_controller.get_selected_configuration() == "Config 3"


def test_add_same_config_again_fails(config_controller: ConfigController):
    add_success1 = config_controller.add_configuration("Config 2")
    config_names1 = config_controller.get_configuration_names()

    add_success2 = config_controller.add_configuration("Config 2")
    config_names2 = config_controller.get_configuration_names()

    assert config_names1 == config_names2

    assert add_success1 is True
    assert add_success2 is False


def test_switch_config(config_controller: ConfigController):
    config_controller.add_configuration("Config 2")
    config_controller.add_configuration("Config 3")
    switch_success = config_controller.switch_configuration("Config 2")

    assert config_controller.get_selected_configuration() == "Config 2"

    assert switch_success is True


def test_switch_non_existing_config_fails(config_controller: ConfigController):
    config_controller.add_configuration("Config 2")
    config_controller.add_configuration("Config 3")
    switch_success = config_controller.switch_configuration("Config 4")

    assert config_controller.get_selected_configuration() == "Config 3"

    assert switch_success is False


def test_config_delete(config_controller: ConfigController):
    config_controller.add_configuration("Config 2")
    config_controller.add_configuration("Config 3")
    delete_success = config_controller.delete_configuration(
        "Config 2")

    config_names = config_controller.get_configuration_names()

    assert "Config 3" in config_names
    assert "Config 2" not in config_names

    assert delete_success is True


def test_delete_non_existing_config_fails(config_controller: ConfigController):
    config_controller.add_configuration("Config 2")
    config_controller.add_configuration("Config 3")

    config_names_before_delete = (
        config_controller.get_configuration_names())

    delete_success = config_controller.delete_configuration(
        "Config 4")

    config_names_after_delete = config_controller.get_configuration_names()

    assert delete_success is False
    assert config_names_before_delete == config_names_after_delete


def test_delete_current_config_switches_to_previous_config(
        config_controller: ConfigController):
    # intended behaviour when deleting the currently selected config is to
    # switch to the config before that
    config_controller.add_configuration("Config 2")
    config_controller.add_configuration("Config 3")
    config_controller.add_configuration("Config 4")
    config_controller.switch_configuration("Config 3")

    delete_success = config_controller.delete_configuration("Config 3")

    assert delete_success is True
    assert config_controller.get_selected_configuration() == "Config 2"


def test_delete_first_config_if_selected_switches_to_second_config(
        config_controller: ConfigController):
    # if the first config is selected and then deleted, intended behaviour
    # is to switch to the second config (which will be the first config
    # after deletion)
    first_config_name = config_controller.get_selected_configuration()
    config_controller.add_configuration("Config 2")
    config_controller.add_configuration("Config 3")
    config_controller.switch_configuration(first_config_name)
    delete_success = config_controller.delete_configuration(first_config_name)

    assert delete_success is True
    assert config_controller.get_selected_configuration() == "Config 2"


def test_config_switched_event_called_on_add(controller: Controller,
                                             config_controller: ConfigController,
                                             mocker: MockerFixture):
    mock_callback = mocker.Mock()
    config_controller.config_switched_event.subscribe(mock_callback)
    config_controller.add_configuration("Config 2")
    mock_callback.assert_called_once_with(
        controller._model.configs["Config 2"])


def test_config_switched_event_not_called_on_failed_add(
        config_controller: ConfigController, mocker: MockerFixture):
    config_controller.add_configuration("Config 2")

    mock_callback = mocker.Mock()
    config_controller.config_switched_event.subscribe(mock_callback)

    # failed add
    config_controller.add_configuration("Config 2")

    mock_callback.assert_not_called()


def test_config_switched_event_called_on_switch(controller: Controller,
                                                config_controller: ConfigController,
                                                mocker: MockerFixture):
    config_controller.add_configuration("Config 2")
    config_controller.add_configuration("Config 3")

    mock_callback = mocker.Mock()
    config_controller.config_switched_event.subscribe(mock_callback)
    config_controller.switch_configuration("Config 2")

    mock_callback.assert_called_once_with(
        controller._model.configs["Config 2"])


def test_config_switched_event_not_called_on_failed_switch(
        config_controller: ConfigController, mocker: MockerFixture):
    config_controller.add_configuration("Config 2")
    config_controller.add_configuration("Config 3")

    mock_callback = mocker.Mock()
    config_controller.config_switched_event.subscribe(mock_callback)

    # failed switch
    config_controller.switch_configuration("Config 4")

    mock_callback.assert_not_called()


def test_config_switch_event_called_on_delete_current_config(
        controller: Controller,
        config_controller: ConfigController,
        mocker: MockerFixture):
    config_controller.add_configuration("Config 2")
    config_controller.add_configuration("Config 3")

    mock_callback = mocker.Mock()
    config_controller.config_switched_event.subscribe(mock_callback)

    config_controller.delete_configuration("Config 3")

    mock_callback.assert_called_once_with(
        controller._model.configs["Config 2"])


def test_config_switch_event_not_called_on_delete_other_config(
        config_controller: ConfigController, mocker: MockerFixture):
    config_controller.add_configuration("Config 2")
    config_controller.add_configuration("Config 3")

    mock_callback = mocker.Mock()
    config_controller.config_switched_event.subscribe(mock_callback)

    config_controller.delete_configuration("Config 2")

    mock_callback.assert_not_called()


def test_get_configuration_names(config_controller):
    first_config_name = config_controller.get_selected_configuration()
    config_controller.add_configuration("Config 3")
    config_controller.add_configuration("Config 2")
    config_controller.add_configuration("Config 0")
    config_controller.add_configuration("Config 4")
    config_controller.delete_configuration("Config 2")
    assert (config_controller.get_configuration_names() ==
            [first_config_name, "Config 3", "Config 0", "Config 4"])
