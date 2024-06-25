import matplotlib.figure
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.ticker import MaxNLocator

from tommy.controller.result_interfaces.correlation_matrix_interface import (
    CorrelationMatrixInterface)
from tommy.controller.topic_modelling_runners.abstract_topic_runner import (
    TopicRunner)
from tommy.controller.visualizations.abstract_visualization import (
    AbstractVisualization)
from tommy.controller.visualizations.possible_visualization import VisGroup
from tommy.controller.visualizations.visualization_input_datatypes import (
    VisInputData)


class CorrelationMatrixCreator(AbstractVisualization):
    """
    A class for (checking the required interfaces for and) constructing a
    correlation matrix plot for topics in the given topic runner and returning
    it as a matplotlib figure.
    """
    _required_interfaces = [CorrelationMatrixInterface, TopicRunner]
    name = 'Correlatiematrix topics'
    short_tab_name = 'Correlatie'
    vis_group = VisGroup.MODEL
    needed_input_data = [VisInputData.PROCESSED_CORPUS]

    def _create_figure(self,
                       topic_runner: TopicRunner | CorrelationMatrixInterface,
                       **kwargs
                       ) -> matplotlib.figure.Figure:
        """
        Construct a correlation matrix plot for the topics in the given
        topic runner and return it as a matplotlib figure.

        :param topic_runner: The topic model to construct the plot for. This
            should implement the CorrelationMatrixInterface
        :return: Matplotlib figure showing a correlation matrix. The matrix
            entries are labeled by their topic_id. A value close to 0 means the
            topics are similar and close to 1 means very different.
        """

        # Construct the correlation matrix
        correlation_matrix = topic_runner.get_correlation_matrix(
            n_words_to_process=30)

        # Construct a plot and axes
        fig, ax = plt.subplots()

        # Construct the correlations matrix adding colors
        data = ax.imshow(correlation_matrix, cmap='Blues',
                         vmin=0, vmax=1,
                         origin='lower')

        # Add a color bar to the plot
        plt.colorbar(data)

        # Add a title and correct integer ticks on both axes
        plt.title(self.name, pad=25)
        ax.yaxis.set_major_locator(MaxNLocator(integer=True))
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))

        # Adjust the plot ticks so that they start from 1 instead of 0
        num_topics = topic_runner.get_n_topics()
        plt.xticks(np.arange(num_topics),
                   np.arange(1, num_topics + 1))
        plt.yticks(np.arange(num_topics),
                   np.arange(1, num_topics + 1))

        fig.figure.subplots_adjust(
            left=0.15, right=0.85, top=0.85, bottom=0.15)

        plt.close()
        return fig


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University
(Department of Information and Computing Sciences)
"""
