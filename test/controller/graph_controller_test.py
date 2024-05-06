import pytest
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from pytest_mock import mocker

from tommy.controller.topic_modelling_controller import (
    TopicModellingController)
from tommy.controller.corpus_controller import (
    CorpusController)
from tommy.controller.graph_controller import (GraphController,
                                               AbstractVisualization,
                                               AbstractVisualizationOnData,
                                               AbstractVisualizationPerTopic)


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
    graph_controller.set_controller_refs(corpus_controller)

    # note: in another branch the setting of topic_modelling_controller
    #   will be moved to set_controller_refs
    graph_controller.set_model_refs(topic_modelling_controller)

    return graph_controller


def test_delete_all_cached_plots(graph_controller: GraphController,
                                 mocker: mocker):
    # Arrange
    method_spies = [mocker.spy(vis, "delete_cache") for
                    vis in (graph_controller.GLOBAL_VISUALIZATIONS +
                            graph_controller.TOPIC_VISUALIZATIONS)]

    # Act
    graph_controller._delete_all_cached_plots()

    # Assert
    for spy in method_spies:
        spy.assert_called_once()
