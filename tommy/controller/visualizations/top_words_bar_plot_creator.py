import matplotlib.figure
from matplotlib import pyplot as plt

from tommy.controller.topic_modelling_runners.abstract_topic_runner import (
    TopicRunner)
from tommy.controller.visualizations.abstract_visualizations_per_topic import (
    AbstractVisualizationPerTopic)
from tommy.datatypes.topics import TopicWithScores

from tommy.support.constant_variables import plot_colors


class TopWordsBarPlotCreator(AbstractVisualizationPerTopic):
    """
    A class for constructing a bar plot for a topics in the given topic runner
    and returning it as a matplotlib figure.
    """
    _required_interfaces = []
    name = 'Woorden met het hoogste gewicht'

    def get_figure(self,
                   topic_runner: TopicRunner,
                   topic_id: int) -> matplotlib.figure.Figure:
        """
        Construct a bar plot matplotlib figure showing
        the top words for the requested topic in the given topic runner.
        :param topic_runner: The topic model to construct the plot for
        :param topic_id: The id of the topic to create the bar plot for
        :return: A bar plot on the top 10 words in the topic showing how much
            each word is associated with the topic.
        """
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

        return fig


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University 
(Department of Information and Computing Sciences)
"""
