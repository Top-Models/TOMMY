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
    vis_group = VisGroup.CORPUS
    needed_input_data = [VisInputData.METADATA_CORPUS]

    def _create_figure(self, topic_runner: TopicRunner | DocumentTopicsInterface,
                       processed_corpus: ProcessedCorpus = None
                       ) -> matplotlib.figure.Figure:

        # 

        for document_id, document in enumerate(processed_corpus):
            document_topic = (
                topic_runner.get_document_topics(document.body.body,
                                                 0.0))


