import matplotlib.figure
from matplotlib import pyplot as plt
from matplotlib.ticker import MaxNLocator

from tommy.controller.result_interfaces.topic_coherence_interface import (
    TopicCoherenceInterface)
from tommy.controller.topic_modelling_runners.abstract_topic_runner import (
    TopicRunner)
from tommy.controller.visualizations.abstract_visualization import (
    AbstractVisualization)
from tommy.controller.visualizations.possible_visualization import VisGroup
from tommy.controller.visualizations.visualization_input_datatypes import (
    VisInputData)
from tommy.support.constant_variables import prim_col_red


class KValueCreator(AbstractVisualization):
    """

    """
    _required_interfaces = [TopicCoherenceInterface, TopicRunner]
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
        axis.plot(topic_range, u_mass, color=f'{prim_col_red}')

        fig.gca().xaxis.set_major_locator(MaxNLocator(integer=True))
        fig.tight_layout()

        fig.figure.subplots_adjust(
            left=0.15, right=0.85, top=0.85, bottom=0.15)

        plt.title(self.name, pad=25)

        plt.close()
        return fig

"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University
(Department of Information and Computing Sciences)
"""
