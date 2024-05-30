import matplotlib.figure
from matplotlib import pyplot as plt
from matplotlib.ticker import MaxNLocator, AutoMinorLocator

from tommy.controller.topic_modelling_runners.abstract_topic_runner import (
    TopicRunner)
from tommy.controller.visualizations.abstract_visualization import (
    AbstractVisualization)
from tommy.controller.visualizations.possible_visualization import VisGroup
from tommy.controller.visualizations.visualization_input_datatypes import (
    VisInputData, MetadataCorpus)
from tommy.support.constant_variables import prim_col_red


class DocumentWordCountCreator(AbstractVisualization):
    """
    A class for constructing a graph showing the number of words per
    documents and returning it as a matplotlib figure.
    """
    _required_interfaces = []
    name = 'Distributie aantal woorden per document'
    short_tab_name = 'Woordaantal'
    vis_group = VisGroup.CORPUS
    needed_input_data = [VisInputData.METADATA_CORPUS]

    def _create_figure(self, topic_runner: TopicRunner,
                       metadata_corpus: MetadataCorpus = None,
                       **kwargs) -> matplotlib.figure.Figure:
        """
        Construct a word count plot showing the number of words per document
        in the given corpus
        :param topic_runner: The topic runner (implementing
            DocumentTopicsInterface) to extract topic data from
        :param metadata_corpus: The metadata of the corpus containing
            data about all documents in the corpus.
        :return: matplotlib figure showing a word count graph
        :raises ValueError: If the metadata_corpus argument is None
        """
        if metadata_corpus is None:
            raise ValueError("Metadata Corpus keyword argument is necessary in"
                             " the document_word_count_creator")

        document_counts = [file.length for file in metadata_corpus]

        # Construct a histogram
        fig, ax = plt.subplots()
        plt.hist(document_counts, bins=150, color=f"{prim_col_red}")

        # Add margins and labels to the plot
        plt.margins(x=0.02)
        plt.xlabel("Aantal woorden per document")
        plt.ylabel("Aantal documenten")
        plt.title("Distributie aantal woorden per document")

        # Use MaxNLocator to ensure the number of ticks is manageable
        ax.xaxis.set_major_locator(MaxNLocator(integer=True, nbins=10))
        ax.yaxis.set_major_locator(MaxNLocator(integer=True, nbins=10))

        # Use AutoMinorLocator to add minor ticks
        ax.xaxis.set_minor_locator(AutoMinorLocator())
        ax.yaxis.set_minor_locator(AutoMinorLocator())

        # Rotate tick labels to prevent overlapping
        plt.xticks(rotation=45)
        plt.yticks(rotation=45)

        fig.figure.subplots_adjust(0.1, 0.1, 0.9, 0.9)

        plt.close()
        return fig


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University
(Department of Information and Computing Sciences)
"""
