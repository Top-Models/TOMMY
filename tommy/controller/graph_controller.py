from itertools import product

import networkx as nx
import matplotlib.figure
import matplotlib.pyplot

# Import controllers
from tommy.controller.corpus_controller import CorpusController
from tommy.controller.topic_modelling_runners.abstract_topic_runner import (
    TopicRunner)
from tommy.controller.topic_modelling_controller import (
    TopicModellingController)

# Import visualizations
from tommy.controller.visualizations.abstract_visualization import (
    AbstractVisualization)
from tommy.controller.visualizations.correlation_matrix_creator import (
    CorrelationMatrixCreator)
from tommy.controller.visualizations.document_topic_network_summary_creator \
    import DocumentTopicNetworkSummaryCreator
from tommy.controller.visualizations.document_word_count_creator import (
    DocumentWordCountCreator)
from tommy.controller.visualizations.top_words_bar_plot_creator import (
    TopWordsBarPlotCreator)
from tommy.controller.visualizations.word_cloud_creator import WordCloudCreator
from tommy.controller.visualizations.word_topic_network_creator import (
    WordTopicNetworkCreator)
from tommy.controller.visualizations.k_value_creator import KValueCreator

# Import exporters
from tommy.controller.visualizations.nx_exporter import NxExporter
from tommy.controller.visualizations.nx_exporter_on_data import (
    NxExporterOnData)
from tommy.controller.visualizations.document_topic_nx_exporter import (
    DocumentTopicNxExporter)
from tommy.controller.visualizations.word_topic_nx_exporter import (
    WordTopicNxExporter)

from tommy.controller.visualizations.possible_visualization import (
    PossibleVisualization)
from tommy.controller.visualizations.visualization_input_datatypes import (
    VisInputData, ProcessedCorpus, MetadataCorpus)

from tommy.datatypes.topics import TopicWithScores
from tommy.model.topic_model import TopicModel
from tommy.support.event_handler import EventHandler


class GraphController:
    """
    The central interface for extracting results from topic modelling results
    and creating visualizations.
    Contains an event for when the plots are changed and a publisher for
    when the topics have changed.
    """
    _topic_modelling_controller: TopicModellingController = None
    _corpus_controller: CorpusController = None

    # Visualization Creators
    VISUALIZATIONS: list[AbstractVisualization] = [
        DocumentWordCountCreator(),
        KValueCreator(),
        CorrelationMatrixCreator(),
        WordTopicNetworkCreator(),
        DocumentTopicNetworkSummaryCreator(),
        WordCloudCreator(),
        TopWordsBarPlotCreator()
    ]
    _possible_visualizations: list[PossibleVisualization] | None = None

    _current_topic_selected_id: int | None = None

    _current_topic_runner: TopicRunner | None = None

    # EventHandlers
    _possible_plots_changed_event: EventHandler[list[PossibleVisualization]]
    _topics_changed_event: EventHandler[None]
    _refresh_plots_event: EventHandler[None]

    # Exporters
    NX_EXPORTS: list[NxExporterOnData | NxExporter] = [
        DocumentTopicNxExporter(),
        WordTopicNxExporter()]
    _possible_nx_exports: list[int] | None = None

    @property
    def possible_plots_changed_event(self) -> EventHandler[
        list[PossibleVisualization]]:
        """Get event that triggers when the list of possible plots changes."""
        return self._possible_plots_changed_event

    @property
    def topics_changed_event(self) -> EventHandler[None]:
        """Get the eventhandler that triggers when the topics are changed."""
        return self._topics_changed_event

    @property
    def refresh_plots_event(self) -> EventHandler[None]:
        """
        Get the event that triggers when the content of any plots changes.
        """
        return self._refresh_plots_event

    @property
    def has_topic_runner(self) -> bool:
        return self._current_topic_runner is not None

    def __init__(self) -> None:
        """Initialize the graph-controller and its two publishers"""
        super().__init__()
        self._possible_plots_changed_event = EventHandler[
            list[PossibleVisualization]]()
        self._topics_changed_event = EventHandler[None]()
        self._refresh_plots_event = EventHandler[None]()

    def set_controller_refs(
            self,
            topic_modelling_controller: TopicModellingController,
            corpus_controller: CorpusController):
        """
        Set reference to the TM controller corpus controller and add self
        to model trained event
        """
        self._corpus_controller = corpus_controller
        self._topic_modelling_controller = topic_modelling_controller

        topic_modelling_controller.model_trained_event.subscribe(
            self.on_topic_runner_complete)
        topic_modelling_controller.topic_model_switched_event.subscribe(
            self._on_config_switch)

    def set_selected_topic(self, topic_index: int | None) -> None:
        """
        Set the currently selected topic to the given index or None if no
        topic is to be selected.

        :param topic_index: the index of the topic to select
        :return: None
        """
        self._current_topic_selected_id = topic_index

        # trigger event to notify that plots may have changed
        self._refresh_plots_event.publish(None)

    def get_number_of_topics(self) -> int:
        """
        Get the number of topics in the topic modelling results
        :return: the number of topics in the topic modelling results
        :raises RuntimeError: if the topic runner has not finished running yet.
        """
        if not self.has_topic_runner:
            raise RuntimeError("Amount of topics requested before topic "
                               "runner has finished running")
        return self._current_topic_runner.get_n_topics()

    def get_topic_with_scores(self, topic_id, n_words) -> TopicWithScores:
        """
        Return a topic object containing top n terms and their corresponding
        score for the topic identified by the topic_id.

        :param topic_id: the index of the requested topic
        :param n_words: number of terms in the resulting topic object
        :return: topic object containing top n terms and their corresponding
            scores
        """
        return self._current_topic_runner.get_topic_with_scores(
            topic_id=topic_id,
            n_words=n_words)

    def _calculate_possible_visualizations(self) -> None:
        """(re-)calculates and saves the list of possible visualizations"""
        # check for each visualization if it is possible
        self._possible_visualizations = [
            PossibleVisualization(vis_index,
                                  visualization.name,
                                  visualization.short_tab_name,
                                  visualization.vis_group,
                                  (VisInputData.TOPIC_ID in
                                   visualization.needed_input_data))
            for (vis_index, visualization)
            in enumerate(self.VISUALIZATIONS)
            if visualization.is_possible(self._current_topic_runner)
        ]

        # check for each export if it is possible
        self._possible_nx_exports = [
            export_index
            for (export_index, exporter)
            in enumerate(self.NX_EXPORTS)
            if exporter.is_possible(self._current_topic_runner)
        ]

    def _get_nx_export(self, vis_index: int) -> nx.graph:
        """
        Returns the networkx graph corresponding showing the network
        corresponding to the given index in the list of all exports.
        :param vis_index: Index of the export to be requested
        :return: networkx graph of a visualization corresponding to the index
        :raises IndexError: if the index is negative or bigger than the number
            of exports supported by this class.
        """
        if vis_index < 0 or vis_index >= len(self.NX_EXPORTS):
            raise IndexError(f'Negative index of {vis_index} is not accepted '
                             'in _get_visualization')

        if isinstance(self.NX_EXPORTS[vis_index], NxExporterOnData):
            return self._run_nx_export_on_data(self.NX_EXPORTS[vis_index])
        if isinstance(self.NX_EXPORTS[vis_index], NxExporter):
            return self._run_nx_export(self.NX_EXPORTS[vis_index])

        # if not, the index is out of range
        raise IndexError(f'No exports with index {vis_index} available')

    def get_visualization(self, vis_index: int,
                          override_topic: int | None = None
                          ) -> matplotlib.figure.Figure:
        """
        Returns the visualization corresponding to the given index in the list
        of all visualizations.
        :param vis_index: Index of the visualization to be requested
        :param override_topic: A topic index used to override the selected
            topic, default to None, which doesn't override the selected topic
        :return: matplotlib figure of visualization corresponding to the index
        :raises IndexError: if the index is negative or bigger than the number
            of visualizations or if the visualization corresponding to that
            index is not possible in the current topic model.
        """
        # if not, the index is out of range
        if vis_index < 0 or vis_index >= len(self.VISUALIZATIONS):
            raise IndexError(f'No visualization with index '
                             f'{vis_index} available')

        vis_creator = self.VISUALIZATIONS[vis_index]
        return self._run_visualization_creator(vis_creator,
                                               override_topic=override_topic)

    def _run_visualization_creator(self, vis_creator: AbstractVisualization,
                                   override_topic: int | None = None
                                   ) -> matplotlib.figure.Figure:
        """
        Returns the given global visualization on the current topic runner and
        the needed additional data.
        :param vis_creator: The visualization creator be run
        :param override_topic: A topic index used to override the selected
            topic, default to None, which doesn't override the selected topic
        :return: matplotlib figure of visualization
        """
        keyword_args = {}
        for arg_needed in vis_creator.needed_input_data:
            match arg_needed:
                case VisInputData.TOPIC_ID if override_topic is not None:
                    keyword_args['topic_id'] = override_topic
                case VisInputData.TOPIC_ID if override_topic is None:
                    if self._current_topic_selected_id is None:
                        return self._get_no_topic_selected_screen()
                    keyword_args['topic_id'] = self._current_topic_selected_id
                case VisInputData.PROCESSED_CORPUS:
                    processed_corpus = (self._corpus_controller.
                                        get_processed_corpus())
                    keyword_args['processed_corpus'] = processed_corpus
                case VisInputData.METADATA_CORPUS:
                    metadata = self._corpus_controller.get_metadata()
                    keyword_args['metadata_corpus'] = metadata
                case _:
                    raise NotImplementedError(f"Unsupported input data "
                                              f"{arg_needed} requested in "
                                              f"visualization "
                                              f"{vis_creator.name}.")

        return vis_creator.get_figure(self._current_topic_runner,
                                      **keyword_args)

    @staticmethod
    def _get_no_topic_selected_screen() -> matplotlib.figure.Figure:
        """Returns a figure showing a text that a topic needs to be selected"""
        fig = matplotlib.pyplot.figure()
        matplotlib.pyplot.figtext(0.5, 0.5, "Selecteer een topic om "
                                            "deze visualizatie te zien",
                                  horizontalalignment='center',
                                  verticalalignment='center')

        fig.figure.subplots_adjust(0.1, 0.1, 0.9, 0.9)
        matplotlib.pyplot.close()
        return fig

    def _run_nx_export_on_data(self, nx_exporter_on_data: NxExporterOnData
                               ) -> nx.Graph:
        """
        Runs the networkx exporter on the additional data that it needs
        :param nx_exporter_on_data: Index of the visualization to be requested
        :return: nx.graph of the exporter
        """

        if nx_exporter_on_data.input_data_type == ProcessedCorpus:
            processed_corpus = self._corpus_controller.get_processed_corpus()
            return nx_exporter_on_data.get_nx_graph(self._current_topic_runner,
                                                    processed_corpus)
        if nx_exporter_on_data.input_data_type == MetadataCorpus:
            metadata = self._corpus_controller.get_metadata()
            return nx_exporter_on_data.get_nx_graph(self._current_topic_runner,
                                                    metadata)

        raise Exception("The graph-controller is asked to supply data of type"
                        f" {nx_exporter_on_data.input_data_type}, which is not"
                        " supported")

    def _run_nx_export(self, nx_exporter: NxExporter) -> nx.Graph:
        """
        Runs the networkx exporter
        :param nx_exporter: Index of the visualization to be requested
        :return: nx.graph of the exporter
        """
        return nx_exporter.get_nx_graph(self._current_topic_runner)

    def get_all_visualizations(self) -> list[matplotlib.figure.Figure]:
        """
        Get all the possible visualization for the current run
        :return: A list of  matplotlib Figures of all possible visualizations
        """
        if self._current_topic_runner is None:
            raise RuntimeError("Plots cannot be requested when topic model "
                               "has not been run.")

        vis_without_topic = [self.get_visualization(possible_vis.index)
                             for possible_vis
                             in self._possible_visualizations
                             if not possible_vis.needs_topic]

        # loop over all topic and all visualization that need topics to
        #   run all combinations
        vis_with_topic = [self.get_visualization(possible_vis.index,
                                                 override_topic=topic_id)
                          for (possible_vis, topic_id)
                          in product(self._possible_visualizations,
                                     range(self.get_number_of_topics()))
                          if possible_vis.needs_topic]

        return vis_without_topic + vis_with_topic

    def get_all_nx_exports(self) -> list[nx.graph]:
        """
        Get all the networkx graphs for the possible visualization for the
        current run
        :return: A list of nx.graph objects of all possible visualizations
        """
        if self._current_topic_runner is None:
            raise RuntimeError("Exports cannot be requested when topic model "
                               "has not been run.")

        return [self._get_nx_export(vis) for vis
                in range(len(self._possible_nx_exports))]

    def _delete_all_cached_plots(self):
        """Delete all cached figures saved by the visualization creators"""
        for vis_creator in self.VISUALIZATIONS:
            vis_creator.delete_cache()

    def on_topic_runner_complete(self, topic_runner: TopicRunner) -> None:
        """
        Signal the graph-controller that a topic runner has finished training
        and is ready to provide results. Notify the subscribes of the plots
        and topics
        :param topic_runner: The newly trained topic runner object
        :return: None
        """
        self._delete_all_cached_plots()
        self._current_topic_runner = topic_runner
        self._calculate_possible_visualizations()
        self._topics_changed_event.publish(None)
        self._possible_plots_changed_event.publish(
            self._possible_visualizations)

    def _on_config_switch(self, topic_runner: TopicRunner):
        self.on_topic_runner_complete(topic_runner)

    def reset_graph_view_state(self) -> None:
        """Reset the state of the graph view"""
        self._current_topic_selected_id = None

    def visualizations_available(self) -> bool:
        """
        Check if there are any visualizations available for the current topic
        model.
        :return: True if there are visualizations available, False otherwise
        """
        return self._current_topic_runner is not None


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University
(Department of Information and Computing Sciences)
"""
