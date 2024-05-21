import matplotlib.figure
from matplotlib import pyplot as plt
from matplotlib.ticker import MaxNLocator

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
    name = 'K-waarde'
    short_tab_name = 'K-waarde'
    vis_group = VisGroup.MODEL
    needed_input_data = [VisInputData.PROCESSED_CORPUS]

    def _create_figure(self,
                       topic_runner: TopicRunner | TopicCoherenceInterface,
                       **kwargs
                       ) -> matplotlib.figure.Figure:
        """
        Construct a k-value plot to see which topic amount is best to optimize
        topics
        :param topic_runner: The topic runner (implementing
            DocumentTopicsInterface) to extract topic data from
        :return: matplotlib figure showing the k-value plot
        """
        # Construct matplotlib figure and axis
        fig, axis = plt.subplots()

        # Calculate coherence scores for the range of topics
        topic_range = range(1, 11)
        u_mass = [topic_runner.get_topic_coherence(num_topics)
                  for num_topics in topic_range]

        # Set the axis and plot figure
        axis.set_xlabel('Aantal topics')
        axis.set_ylabel('$u_{mass}$')
        axis.plot(topic_range, u_mass, color='darkblue')

        fig.gca().xaxis.set_major_locator(MaxNLocator(integer=True))
        fig.tight_layout()

        plt.close()
        return fig

