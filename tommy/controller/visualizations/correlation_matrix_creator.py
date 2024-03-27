import matplotlib.figure
from matplotlib import pyplot as plt
from matplotlib.ticker import MaxNLocator

from tommy.controller.result_interfaces.correlation_matrix_interface import (
    CorrelationMatrixInterface)
from tommy.controller.topic_modelling_runners.abstract_topic_runner import (
    TopicRunner)

from tommy.controller.visualizations.abstract_visualization import (
    AbstractVisualization)


class CorrelationMatrixCreator(AbstractVisualization):
    """
    A class for (checking the required interfaces for and) constructing a
    correlation matrix plot for topics in the given topic runner and returning
    it as a matplotlib figure.
    """
    _required_interfaces = [CorrelationMatrixInterface]
    name = 'Correlatiematrix topics'

    def get_figure(self,
                   topic_runner: TopicRunner | CorrelationMatrixInterface
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
        correlation_matrix = topic_runner.get_correlation_matrix(20)

        # Construct a plot and axes
        fig, ax = plt.subplots()

        # Construct the correlations matrix adding colors
        data = ax.imshow(correlation_matrix, cmap='RdBu_r', origin='lower')

        # Add a color bar to the plot
        plt.colorbar(data)

        # Add a title and correct integer ticks on both axes
        plt.title(self.name)
        fig.gca().yaxis.set_major_locator(MaxNLocator(integer=True))
        fig.gca().xaxis.set_major_locator(MaxNLocator(integer=True))

        return fig


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University 
(Department of Information and Computing Sciences)
"""
