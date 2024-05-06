from typing import TypeAliasType

import matplotlib.figure
import networkx as nx
from matplotlib import pyplot as plt

from tommy.controller.topic_modelling_runners.abstract_topic_runner import (
    TopicRunner)
from tommy.datatypes.topics import Topic, TopicWithScores
from tommy.controller.file_import.processed_file import ProcessedFile
from tommy.controller.visualizations.abstract_visualization_on_data import (
        AbstractVisualizationOnData)
from tommy.controller.visualizations.visualization_input_datatypes import (
    MetadataCorpus)


class DocumentWordCountCreator(
        AbstractVisualizationOnData[MetadataCorpus]):
    """
    A class for constructing a graph showing the number of words per
    documents and returning it as a matplotlib figure.
    """
    _required_interfaces = []
    name = 'Distributie aantal woorden per document'

    @property
    def input_data_type(self) -> TypeAliasType:
        """Returns the type of the additional data needed in get_figure"""
        return MetadataCorpus

    def _create_figure(self,
                       topic_runner: TopicRunner,
                       data: MetadataCorpus
                       ) -> matplotlib.figure.Figure:
        """
        Construct a word count plot showing the number of words per document
        in the given corpus
        :param topic_runner: The topic runner (implementing
            DocumentTopicsInterface) to extract topic data from
        :param data: The metadata of the corpus containing
            data about all documents in the corpus.
        :return: matplotlib figure showing a word count graph
        """

        document_counts = [file.length for file in data]

        # Construct a histogram
        fig = plt.figure()
        plt.hist(document_counts, bins=150, color="darkblue")

        # Add margins and labels to the plot
        plt.margins(x=0.02)
        plt.xlabel("aantal woorden per document")
        plt.ylabel("aantal documenten")
        plt.title("Distributie aantal woorden per document")

        plt.close()
        return fig


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University 
(Department of Information and Computing Sciences)
"""
