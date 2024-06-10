from random import random

import matplotlib.figure
from matplotlib import pyplot as plt
from wordcloud import WordCloud

from tommy.controller.topic_modelling_runners.abstract_topic_runner import (
    TopicRunner)
from tommy.controller.visualizations.abstract_visualization import (
    AbstractVisualization)
from tommy.datatypes.topics import TopicWithScores
from tommy.controller.visualizations.possible_visualization import VisGroup
from tommy.controller.visualizations.visualization_input_datatypes import (
    VisInputData, TopicID)
from tommy.support.constant_variables import emma_colors


class WordCloudCreator(AbstractVisualization):
    """
    A class for constructing a word cloud for the topic in the given topic
    runner and returning it as a matplotlib figure.
    """
    _required_interfaces = [TopicRunner]
    name = 'Woordenwolk'
    short_tab_name = 'Woordenwolk'
    vis_group = VisGroup.TOPIC
    needed_input_data = [VisInputData.TOPIC_ID]

    def _create_figure(self,
                       topic_runner: TopicRunner,
                       topic_id: TopicID = None,
                       **kwargs) -> matplotlib.figure.Figure:
        """
        Construct a wordcloud matplotlib figure for the requested topics in the
        given topic runner.
        :param topic_runner: The topic model to construct the plot for.
        :param topic_id: The id of the topic to create the word cloud for.
        :return: A wordcloud on words in the topic where the size of the words
            is determined by how much they align with the topic. The colors on
            the word cloud do not convey information about the words.
        :raises ValueError: If the topic_id argument is None.
        """
        if topic_id is None:
            raise ValueError("topic_id keyword argument is necessary in"
                             " the word_cloud_creator")

        topic = topic_runner.get_topic_with_scores(topic_id, 30)
        word_to_score_dict = dict(topic.top_words_with_scores)

        # Define a color function that returns a random color
        def color_func(word, font_size, position, orientation,
                       random_state=None, **kwargs):
            return emma_colors[int(random() * len(emma_colors))]

        wordcloud = (WordCloud(width=1800,
                               height=900,
                               background_color='white',
                               color_func=color_func).
                     generate_from_frequencies(word_to_score_dict))

        # Construct a word cloud
        fig = plt.figure()
        plt.title("Woordenwolk topic {}".format(topic_id + 1), pad=25)
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')

        fig.figure.subplots_adjust(0.1, 0.1, 0.9, 0.9)

        plt.close()
        return fig


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University
(Department of Information and Computing Sciences)
"""
