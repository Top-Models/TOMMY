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
        given topic runner
        :param topic_runner: The topic model to construct the plot for
        :param topic_id: The id of the topic to create the word cloud for
        :return: A wordcloud on words in the topic where the size of the words
            is determined by how much they align with the topic. The colors on
            the word cloud do not convey information about the words.
        :raises ValueError: If the topic_id argument is None
        """
        if topic_id is None:
            raise ValueError("topic_id keyword argument is necessary in"
                             " the word_cloud_creator")

        topic = topic_runner.get_topic_with_scores(topic_id, 30)
        word_to_score_dict = dict(topic.top_words_with_scores)

        wordcloud = (WordCloud(width=800,
                               height=400,
                               background_color='white').
                     generate_from_frequencies(dict(word_to_score_dict)))

        # Construct a word cloud
        fig = plt.figure()
        plt.title("Woordenwolk topic {}".format(topic_id + 1))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.tight_layout(pad=0)

        fig.figure.subplots_adjust(0.1, 0.1, 0.9, 0.9)

        plt.close()
        return fig


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University
(Department of Information and Computing Sciences)
"""
