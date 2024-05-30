import matplotlib.figure
from matplotlib import pyplot as plt
import matplotlib.dates
import pandas as pd
import numpy as np
from datetime import date, datetime
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

from tommy.support.constant_variables import plot_colors


class DocumentsOverTimeCreator(AbstractVisualization):

    _required_interfaces = [TopicRunner]
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
        fig, ax = plt.subplots()

        for topic_id in range(topic_runner.get_n_topics()):
            dates = {"date": [],
                     "probability": []}
            for document in processed_corpus:
                if (document.metadata.date is not None):
                    current_date = datetime.combine(document.metadata.date,
                                                    datetime.min.time())
                    topics = topic_runner.get_document_topics(document.body.body,
                                                              0.0)

                    topic = [topic for topic in topics if topic[0] == topic_id]
                    if topic:
                        current_probability = topic[0][1]
                    else:
                        current_probability = 0.0
                    dates["date"].append(current_date)
                    dates["probability"].append(current_probability)

            if all([dates[i] == [] for i in dates]):
                return self._get_no_dates_available_screen()

            df = pd.DataFrame(dates)
            df = df.groupby("date", as_index=False).sum()
            df = df.sort_values(by="date", ascending=True)
            grouped_df = self._group_df(df)

            ax.plot(grouped_df["date"],
                    grouped_df["probability"],
                    color=plot_colors[topic_id % len(plot_colors)],
                    label=topic_id + 1)

            plt.title("Documenten over tijd topic {}".format(topic_id + 1))
            plt.xlabel("Datum")
            plt.ylabel("Som gewichten")
            plt.xticks(rotation=30)

            ax.legend()

        return fig

    @staticmethod
    def _get_no_dates_available_screen() -> matplotlib.figure.Figure:
        """Returns a figure showing a text that there are no dates available."""
        fig = plt.figure()
        plt.figtext(0.5,
                    0.5,
                    "Er zijn geen datums in de dataset om te laten zien",
                    horizontalalignment='center',
                    verticalalignment='center')

        fig.subplots_adjust(0.1, 0.1, 0.9, 0.9)
        plt.close()
        return fig

    @staticmethod
    def _get_valid_offsets() -> list[str]:
        return ["YE", "6ME", "2ME", "ME", "2W", "W", "D", "6h", "h", "min",
                "s"]

    @staticmethod
    def _group_df(df: pd.DataFrame) -> pd.DataFrame:
        offsets = DocumentsOverTimeCreator._get_valid_offsets()

        for offset in offsets:
            new_df = df.groupby([pd.Grouper(key='date', freq=offset)],
                                as_index=False)["probability"].sum()
            if new_df.shape[0] >= 12:
                return new_df

        return df.groupby([pd.Grouper(key='date', freq="ME")],
                          as_index=False)["probability"].sum()