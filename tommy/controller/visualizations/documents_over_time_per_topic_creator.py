import matplotlib.figure
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib import dates as dts
from matplotlib.ticker import MaxNLocator
from datetime import datetime

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


class DocumentsOverTimePerTopicCreator(AbstractVisualization):
    _required_interfaces = []
    name = 'Documenten over tijd'
    short_tab_name = 'Doc. over tijd'
    vis_group = VisGroup.TOPIC
    needed_input_data = [VisInputData.TOPIC_ID, VisInputData.PROCESSED_CORPUS]

    def _create_figure(self,
                       topic_runner: TopicRunner | DocumentTopicsInterface,
                       topic_id: TopicID = None,
                       processed_corpus: ProcessedCorpus = None,
                       **kwargs
                       ) -> matplotlib.figure.Figure:

        if topic_id is None:
            raise ValueError("topic_id keyword argument is necessary in"
                             " the documents_over_time_per_topic_creator")

        # Construct a plot and axes
        fig, ax = plt.subplots()

        dates = {"date": [],
                 "probability": []}
        for document in processed_corpus:
            current_date = datetime.combine(document.metadata.date,
                                            datetime.min.time())
            topics = topic_runner.get_document_topics(document.body.body, 0.0)

            topic = [topic for topic in topics if topic[0] == topic_id]
            if topic:
                current_probability = topic[0][1]
                dates["date"].append(current_date)
                dates["probability"].append(current_probability)

        df = pd.DataFrame(dates)
        df = df.groupby("date", as_index=False).sum()
        df = df.sort_values(by="date", ascending=True)
        df = df.groupby([pd.Grouper(key='date', freq='ME')], as_index=False)[
            "probability"].sum()

        ax.plot(df["date"],
                df["probability"],
                color=plot_colors[topic_id % len(plot_colors)])

        plt.title("Documenten over tijd topic {}".format(topic_id + 1))
        plt.xlabel("Datum")
        plt.ylabel("Som gewichten")
        plt.xticks(rotation=30)

        return fig
