import matplotlib.figure
from matplotlib import pyplot as plt

from tommy.controller.topic_modelling_runners.abstract_topic_runner import (
    TopicRunner)
from tommy.controller.file_import.processed_file import ProcessedFile
from tommy.controller.visualizations.abstract_visualization import (
        AbstractVisualization)
from tommy.controller.visualizations.possible_visualization import VisGroup
from tommy.controller.visualizations.visualization_input_datatypes import (
    VisInputData, MetadataCorpus)

from tommy.datatypes.topics import Topic, TopicWithScores


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
        fig = plt.figure()
        plt.hist(document_counts, bins=150, color="darkblue")

        # Add margins and labels to the plot
        plt.margins(x=0.02)
        plt.xlabel("aantal woorden per document")
        plt.ylabel("aantal documenten")
        plt.title("Distributie aantal woorden per document")

        fig.figure.subplots_adjust(0.1, 0.1, 0.9, 0.9)

        plt.close()
        return fig


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University
(Department of Information and Computing Sciences)
"""
