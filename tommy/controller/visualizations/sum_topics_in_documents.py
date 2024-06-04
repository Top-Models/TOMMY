import matplotlib.figure
from matplotlib import pyplot as plt
from matplotlib.ticker import MaxNLocator
import pandas as pd

from tommy.controller.result_interfaces.document_topics_interface import (
    DocumentTopicsInterface)
from tommy.controller.topic_modelling_runners.abstract_topic_runner import (
    TopicRunner)
from tommy.controller.visualizations.possible_visualization import VisGroup
from tommy.controller.visualizations.visualization_input_datatypes import (
    VisInputData, MetadataCorpus, TopicID, ProcessedCorpus)

from tommy.controller.visualizations.abstract_visualization import (
    AbstractVisualization)

from tommy.support.constant_variables import plot_colors


class SumTopicsInDocuments(AbstractVisualization):

    _required_interfaces = [TopicRunner]
    name = "Topics in documenten"
    short_tab_name = "Topics in doc."
    vis_group = VisGroup.MODEL
    needed_input_data = [VisInputData.PROCESSED_CORPUS]

    def _create_figure(self,
                       topic_runner: TopicRunner | DocumentTopicsInterface,
                       processed_corpus: ProcessedCorpus = None,
                       **kwargs
                       ) -> matplotlib.figure.Figure:
        """
        Construct a plot containing the sum of all probabilities for each
        topic.

        :param topic_runner: The topic model to construct the plot for. This
            should implement the DocumentTopicsInterface.
        :param processed_corpus: The preprocessed corpus containing all files
            as bags of words after preprocessing.
        :return: Matplotlib figure showing a sum topics in documents plot.
        """

        # Construct a plot and axes
        fig, ax = plt.subplots()

        doc_info = {"topic_id": [],
                    "probability": []}

        for document in processed_corpus:
            topics = topic_runner.get_document_topics(document.body.body, 0.0)
            for topic in topics:
                doc_info["topic_id"].append(topic[0])
                doc_info["probability"].append(topic[1])

        df = pd.DataFrame(doc_info)
        df = df.groupby(by="topic_id", as_index=False).sum()

        plt.bar(df["topic_id"] + 1, df["probability"], color=plot_colors)
        plt.title("Verdeling topics over documenten")
        plt.xlabel("Topic")
        plt.ylabel("Som kansen")

        fig.gca().xaxis.set_major_locator(MaxNLocator(integer=True))

        return fig

