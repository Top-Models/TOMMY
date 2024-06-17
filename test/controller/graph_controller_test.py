import pytest
from gensim.models import LdaModel
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from pytest_mock import mocker, MockerFixture

from tommy.controller.file_import.processed_body import ProcessedBody
from tommy.controller.file_import.processed_corpus import ProcessedCorpus
from tommy.controller.file_import.processed_file import ProcessedFile
from tommy.controller.project_settings_controller import (
    ProjectSettingsController)
from tommy.controller.topic_modelling_controller import (
    TopicModellingController)
from tommy.controller.corpus_controller import (
    CorpusController)
from tommy.controller.graph_controller import (GraphController,
                                               PossibleVisualization,
                                               TopicWithScores,
                                               VisInputData,
                                               AbstractVisualization)
from tommy.controller.topic_modelling_runners.abstract_topic_runner import \
    TopicRunner
from tommy.controller.topic_modelling_runners.lda_runner import LdaRunner
from tommy.model.topic_model import TopicModel


@pytest.fixture(scope='function')
def plot() -> Figure:
    canvas = Figure()
    canvas.add_subplot(111)
    plt.close()
    return canvas


@pytest.fixture(scope='function')
def graph_controller() -> GraphController:
    graph_controller = GraphController()

    topic_modelling_controller = TopicModellingController()
    corpus_controller = CorpusController()
    project_settings_controller = ProjectSettingsController()
    graph_controller.set_controller_refs(topic_modelling_controller,
                                         corpus_controller,
                                         project_settings_controller)

    return graph_controller


@pytest.mark.parametrize("topic_id", [(5,), (1,), (0,), (None,)])
def test_set_selected_topic(graph_controller: GraphController, topic_id: int):
    # Act
    graph_controller.set_selected_topic(topic_id)

    # Assert
    if topic_id is None:
        assert graph_controller is None
    else:
        assert graph_controller._current_topic_selected_id == topic_id


@pytest.mark.parametrize("n_topics", [(5,), (1,), (2,), (999,)])
def test_get_number_of_topics(graph_controller: GraphController, n_topics: int,
                              mocker: MockerFixture):
    # Arrange
    mock_topic_runner = mocker.Mock()
    graph_controller._current_topic_runner = mock_topic_runner
    mocker.patch.object(graph_controller._current_topic_runner, "get_n_topics",
                        return_value=n_topics)

    # Assert
    assert graph_controller.get_number_of_topics() == n_topics


@pytest.fixture(scope='function')
def words_with_scores() -> list[tuple[str, float]]:
    return list(zip(
        ["word1", "word2", "s", "LONG WORD WITH SPACES", "5", "SIX",
         "7", "8", "9", "10", "11", "12", "13", "14", "15"],
        [0.8394117569613936, 0.803704272713246, 0.7547414141744883,
         0.7403765400825127, 0.5650882510726273, 0.5530634246164807,
         0.40274019930419425, 0.3914758433804091, 0.3750981383670168,
         0.37434481176028456, 0.3474111786756603, 0.261372515313952,
         0.15334319058401957, 0.11094254775589907, 0.01655544573469466]))


@pytest.mark.parametrize("topic_id, n_words", [(5, 15), (1, 3), (2, 7),
                                               (999, 13)])
def test_get_topic_with_scores(graph_controller: GraphController,
                               topic_id: int, n_words: int,
                               words_with_scores,
                               mocker: MockerFixture):
    # Arrange
    mock_topic_runner = mocker.Mock()
    graph_controller._current_topic_runner = mock_topic_runner
    mocker.patch.object(graph_controller._current_topic_runner,
                        "get_topic_with_scores",
                        return_value=TopicWithScores(topic_id,
                                                     words_with_scores[:n_words
                                                     ]))

    # Assert
    topic = graph_controller.get_topic_with_scores(topic_id, n_words)
    assert topic.topic_id == topic_id
    assert topic.top_words_with_scores == words_with_scores[:n_words]


@pytest.mark.parametrize("vis_index, override_topic",
                         [(5, None), (1, 3), (2, 7), (999, None)])
def test_get_visualization(plot: Figure, graph_controller: GraphController,
                           vis_index: int, override_topic: int | None,
                           mocker: MockerFixture):
    # Arrange
    mocked_method: mocker = mocker.patch.object(
        graph_controller,
        "_run_visualization_creator",
        return_value=plot)

    # Act
    try:
        graph_controller.get_visualization(vis_index, override_topic)
    except IndexError:
        # Assert - should only raise error if index actually out of bounds
        assert vis_index < 0 or vis_index >= len(
            graph_controller.VISUALIZATIONS)
    else:
        # Assert - that run_visualization is called once with correct params
        mocked_method.assert_called_once_with(
            graph_controller.VISUALIZATIONS[vis_index],
            override_topic=override_topic,
            ignore_cache=False)


@pytest.mark.parametrize("needed_input_data, override_topic",
                         [([VisInputData.TOPIC_ID,
                            VisInputData.METADATA_CORPUS], None),
                          ([VisInputData.PROCESSED_CORPUS,
                            VisInputData.METADATA_CORPUS,
                            VisInputData.TOPIC_ID], 3),
                          ([], 7), ([], None)])
def test_run_visualization_creator(plot: Figure,
                                   graph_controller: GraphController,
                                   needed_input_data: [VisInputData],
                                   override_topic: int | None,
                                   mocker: MockerFixture):
    # Arrange - mock abstract_visualization
    mocked_graph_creator: AbstractVisualization = mocker.Mock()
    mocked_graph_creator.needed_input_data = needed_input_data
    mocked_method: mocker = mocker.patch.object(mocked_graph_creator,
                                                "get_figure",
                                                return_value=plot)

    # mock data
    mock_data = {VisInputData.TOPIC_ID: ('topic_id', 0),
                 VisInputData.METADATA_CORPUS: ('metadata_corpus',
                                                'mock_metadata'),
                 VisInputData.PROCESSED_CORPUS: ('processed_corpus',
                                                 'mock_corpus')}

    # mock all necessary data
    mocker.patch.object(graph_controller._corpus_controller,
                        "get_processed_corpus", return_value="mock_corpus")
    mocker.patch.object(graph_controller._corpus_controller,
                        "get_metadata", return_value="mock_metadata")
    graph_controller._current_topic_selected_id = 0

    # Act
    graph_controller._run_visualization_creator(mocked_graph_creator,
                                                override_topic)

    # Arrange - create dict of expected arguments passed to visualization
    expected_args = {}
    for vis_data in needed_input_data:
        arg_name, mock_arg_value = mock_data[vis_data]
        if vis_data == VisInputData.TOPIC_ID and override_topic is not None:
            expected_args[arg_name] = override_topic
        else:
            expected_args[arg_name] = mock_arg_value

    # Assert - that visualization is called with expected arguments
    mocked_method.assert_called_once_with(
        graph_controller._current_topic_runner,
        ignore_cache=False,
        **expected_args)


def test_delete_all_cached_plots(graph_controller: GraphController,
                                 mocker: MockerFixture):
    # Arrange
    method_spies = [mocker.spy(vis, "delete_cache")
                    for vis in graph_controller.VISUALIZATIONS]

    # Act
    graph_controller._delete_all_cached_plots()

    # Assert
    for spy in method_spies:
        spy.assert_called_once()


def test_reset_graph_view_state(graph_controller: GraphController,
                                mocker: MockerFixture):
    # Arrange
    mocker.patch.object(graph_controller, "_delete_all_cached_plots")
    mocker.patch.object(graph_controller, "_current_topic_selected_id", 5)

    # Act
    graph_controller.reset_graph_view_state()

    # Assert
    assert graph_controller._current_topic_selected_id is None


def test_visualizations_available(graph_controller: GraphController):
    graph_controller._current_topic_runner = None
    assert not graph_controller.visualizations_available()

    topic_model = TopicModel()

    processed_corpus = ProcessedCorpus()
    processed_corpus.documents = [
        ProcessedFile(None, ProcessedBody([f"doc{i}"])) for i in range(10)]

    graph_controller._current_topic_runner = LdaRunner(topic_model,
                                                       processed_corpus, 0, 5)

    assert graph_controller.visualizations_available()


def test_set_current_config(graph_controller: GraphController):
    config_name = "test_config"
    graph_controller.set_current_config(config_name)
    assert graph_controller._current_config == config_name


def test_get_topic_name(graph_controller: GraphController,
                        mocker: MockerFixture):
    topic_index = 0
    topic_name = "test_topic"
    mocker.patch.object(graph_controller._topic_name_model,
                        "get_topic_name", return_value=topic_name)
    graph_controller._current_config = "test_config"
    assert graph_controller.get_topic_name(topic_index) == topic_name


def test_set_topic_name(graph_controller: GraphController,
                        mocker: MockerFixture):
    topic_index = 0
    topic_name = "test_topic"
    mock_set_topic_name = mocker.patch.object(
            graph_controller._topic_name_model, "set_topic_name")
    graph_controller._current_config = "test_config"
    graph_controller.set_topic_name(topic_index, topic_name)
    mock_set_topic_name.assert_called_once_with("test_config",
                                                topic_index, topic_name)


def test_remove_config(graph_controller: GraphController,
                       mocker: MockerFixture):
    config_name = "test_config"
    mock_remove_config = mocker.patch.object(
            graph_controller._topic_name_model, "remove_config")
    graph_controller.remove_config(config_name)
    mock_remove_config.assert_called_once_with(config_name)


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University
(Department of Information and Computing Sciences)
"""
