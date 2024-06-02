import pytest

from tommy.controller.controller import Controller


@pytest.fixture
def controller() -> Controller:
    return Controller()


def test_run_without_error(controller: Controller) -> None:
    # test if topic modelling can run without error
    controller.project_settings_controller.set_input_folder_path(
        "../test/test_data/test_pdf_files/correct_files")
    controller.on_run_topic_modelling()
    assert controller.graph_controller.has_topic_runner is True
