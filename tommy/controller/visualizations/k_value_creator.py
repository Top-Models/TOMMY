import matplotlib.figure
from matplotlib import pyplot as plt

from tommy.controller.result_interfaces.topic_coherence_interface import (
    TopicCoherenceInterface)
from tommy.controller.visualizations.abstract_visualization import (
    AbstractVisualization)
from tommy.controller.topic_modelling_runners.abstract_topic_runner import (
    TopicRunner)
from tommy.controller.visualizations.possible_visualization import VisGroup
from tommy.controller.visualizations.visualization_input_datatypes import (
    VisInputData, TopicID, MetadataCorpus, ProcessedCorpus)


class KValueCreator(AbstractVisualization):
    """

    """
    _required_interfaces = [TopicCoherenceInterface]
    name = 'K-value'
    short_tab_name = 'K-value'
    vis_group = VisGroup.MODEL
    needed_input_data = [VisInputData.PROCESSED_CORPUS]

    def _create_figure(self,
                       topic_runner: TopicRunner | TopicCoherenceInterface,
                       **kwargs
                       ) -> matplotlib.figure.Figure:
        fig = plt.figure()
        x = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        y = [1, 4, 5, 3, 7, 8, 12, 2, 1]
        plt.plot(x, y)
        return fig

