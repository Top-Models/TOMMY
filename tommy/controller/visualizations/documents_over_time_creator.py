import matplotlib.figure
from matplotlib import pyplot as plt
from matplotlib.ticker import MaxNLocator

from tommy.controller.result_interfaces.document_topics_interface import (
    DocumentTopicsInterface)
from tommy.controller.topic_modelling_runners.abstract_topic_runner import (
    TopicRunner)
from tommy.controller.visualizations.possible_visualization import VisGroup
from tommy.controller.visualizations.visualization_input_datatypes import (
    VisInputData, MetadataCorpus, TopicID, ProcessedCorpus)

from tommy.controller.visualizations.abstract_visualization import (
    AbstractVisualization)


class DocumentsOverTimeCreator(AbstractVisualization):

    _required_interfaces = []
    name = 'Documenten over tijd'
    short_tab_name = 'Doc. over tijd'
    vis_group = VisGroup.MODEL
    needed_input_data = [VisInputData.PROCESSED_CORPUS]

    def _create_figure(self,
                       topic_runner: TopicRunner | DocumentTopicsInterface,
                       processed_corpus: ProcessedCorpus = None,
                       **kwargs
                       ) -> matplotlib.figure.Figure:

        # Construct a plot and axes
        figure, ax = plt.subplots()

        years = [(document.metadata.date, document) for document in processed_corpus]

        result = {}

        #for year in years:

        #fjdks = [ for year in years]






        topic_sum = [0] * topic_runner.get_n_topics()

        for document_id, document in enumerate(processed_corpus):
            document_topic = (
                topic_runner.get_document_topics(document.body.body,
                                                 0.0))
            for (topic_id, probability) in document_topic:
                topic_sum[topic_id] += probability

        ax.plot(range(1, topic_runner.get_n_topics() + 1), topic_sum)

        return figure




