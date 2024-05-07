import pytest
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from pytest_mock import mocker

from tommy.controller.visualizations.abstract_visualization import (
    AbstractVisualization, TopicRunner, VisGroup, VisInputData, TopicID)

# create test plot
test_plot = Figure()
test_plot.add_subplot(111)
plt.close()


@pytest.fixture(scope='function')
def plot() -> Figure:
    return test_plot


class MockVisualization(AbstractVisualization):
    _required_interfaces = []
    name = "MockVisualization"
    short_tab_name: str = "Mock"
    vis_group: VisGroup = VisGroup.TOPIC
    needed_input_data: list[VisInputData] = [VisInputData.TOPIC_ID]

    def _create_figure(self,
                       topic_runner: TopicRunner,
                       topic_id: TopicID = None,
                       **kwargs) -> Figure:
        return test_plot


@pytest.fixture(scope='function')
def mock_visualization() -> MockVisualization:
    return MockVisualization()


@pytest.mark.parametrize("topic_id, cached_plot", [(5, test_plot), (1, None),
                                                   (2, test_plot), (999, None)]
                         )
def test_get_figure(mock_visualization: MockVisualization,
                    topic_id: int, cached_plot: Figure | None, plot,
                    mocker):
    # Arrange
    mocked_cache_method = mocker.patch.object(mock_visualization,
                                              "_get_cached_figure",
                                              return_value=cached_plot)
    mock_topic_runner: TopicRunner = mocker.Mock()
    mocked_create_figure_method = mocker.patch.object(
        mock_visualization,
        "_create_figure",
        return_value=plot)

    # Act
    mock_visualization.get_figure(mock_topic_runner,
                                  topic_id=topic_id)

    # Assert
    mocked_cache_method.assert_called_once_with(topic_id=topic_id)
    if cached_plot is None:
        # assert that new plot is calculated with the correct arguments
        mocked_create_figure_method.assert_called_once()
        args, kwargs = mocked_create_figure_method.call_args
        assert kwargs['topic_id'] == topic_id
        assert kwargs['topic_runner'] == mock_topic_runner

        # assert that the new plot is saved in cache
        mocker.stop(mocked_cache_method)
        assert mock_visualization._get_cached_figure(
            topic_id=topic_id) == plot
    else:
        # assert that figure was not recalculated unnecessariliy
        mocked_create_figure_method.assert_not_called()


@pytest.mark.parametrize("topic_id", [(5,), (1,), (2,), (999,)])
def test_cache(mock_visualization: MockVisualization,
               topic_id: int, plot, mocker):
    # Arrange
    mock_topic_runner: TopicRunner = mocker.Mock()

    # Assert that initially there is no cache
    assert (mock_visualization.
            _get_cached_figure(topic_id=topic_id) is None)

    # Act - generate cache
    mock_visualization.get_figure(mock_topic_runner,
                                  topic_id=topic_id)

    # Assert - that there is now cache
    assert (mock_visualization.
            _get_cached_figure(topic_id=topic_id) is plot)

    # Act - delete cache
    mock_visualization.delete_cache()

    # Assert - that there is no cache again
    assert (mock_visualization.
            _get_cached_figure(topic_id=topic_id) is None)
