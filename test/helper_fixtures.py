import pytest
from pytest_mock import MockerFixture

from tommy.controller.controller import Controller


@pytest.fixture
def controller_no_pipeline(mocker: MockerFixture) -> Controller:
    """
    Fixture for a Controller that doesn't load the preprocessing pipeline.
    Loading the pipeline takes a long time and is not necessary for most
    tests, therefore most tests that require an instance of the Controller
    can use this one instead.
    """
    with mocker.patch('tommy.controller.preprocessing_controller'
                      '.PreprocessingController.load_pipeline'):
        return Controller()
