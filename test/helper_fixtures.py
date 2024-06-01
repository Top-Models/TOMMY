import pytest
from pytest_mock import MockerFixture

from tommy.controller.controller import Controller


@pytest.fixture
def controller_no_pipeline(mocker: MockerFixture):
    with mocker.patch('tommy.controller.preprocessing_controller'
                      '.PreprocessingController.load_pipeline'):
        return Controller()
