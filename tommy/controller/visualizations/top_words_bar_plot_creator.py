import matplotlib.figure
from matplotlib import pyplot as plt

from tommy.controller.topic_modelling_runners.abstract_topic_runner import (
    TopicRunner)
from tommy.controller.visualizations.abstract_visualization import (
    AbstractVisualization)
from tommy.datatypes.topics import TopicWithScores
from tommy.controller.visualizations.possible_visualization import VisGroup
from tommy.controller.visualizations.visualization_input_datatypes import (
    VisInputData, TopicID)

from tommy.support.constant_variables import plot_colors


class TopWordsBarPlotCreator(AbstractVisualization):
    """
    A class for constructing a bar plot for a topics in the given topic runner
    and returning it as a matplotlib figure.
    """
    _required_interfaces = []
    name = 'Woorden met het hoogste gewicht'
    short_tab_name = 'Woordgewichten'
    vis_group = VisGroup.TOPIC
    needed_input_data = [VisInputData.TOPIC_ID]

    def _create_figure(self,
                       topic_runner: TopicRunner,
                       topic_id: TopicID = None,
                       **kwargs) -> matplotlib.figure.Figure:
        """
        Construct a bar plot matplotlib figure showing
        the top words for the requested topic in the given topic runner.
        :param topic_runner: The topic model to construct the plot for
        :param topic_id: The id of the topic to create the bar plot for
        :return: A bar plot on the top 10 words in the topic showing how much
            each word is associated with the topic.
        :raises ValueError: If the topic_id argument is None
        """
        if topic_id is None:
            raise ValueError("topic_id keyword argument is necessary in"
                             " the top_words_bar_plot_creator")

        topic = topic_runner.get_topic_with_scores(topic_id=topic_id,
                                                   n_words=15)

        # Construct a horizontal bar plot
        fig = plt.figure()
        plt.barh(topic.top_words,
                 topic.word_scores,
                 color=plot_colors[topic_id % len(plot_colors)])
        plt.gca().invert_yaxis()

        # Add margins and labels to the plot
        plt.margins(0.02)
        plt.xlabel("gewicht")
        plt.title(f"Woorden met het hoogste gewicht topic {topic_id+1}")

        fig.figure.subplots_adjust(0.2, 0.2, 0.8, 0.8)

        plt.close()
        return fig


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University
(Department of Information and Computing Sciences)
"""
