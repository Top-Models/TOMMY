import matplotlib.figure
from matplotlib import pyplot as plt
import matplotlib.dates
import pandas as pd
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
        fig, ax = plt.subplots()

        for topic_id in range(topic_runner.get_n_topics()):
            dates = {"date": [],
                     "probability": []}
            for document in processed_corpus:
                current_date = datetime.combine(document.metadata.date,
                                                datetime.min.time())
                topics = topic_runner.get_document_topics(document.body.body,
                                                          0.0)
                current_probability = topics[topic_id][1]
                dates["date"].append(current_date)
                dates["probability"].append(current_probability)

            df = pd.DataFrame(dates)
            df = df.groupby("date", as_index=False).sum()
            df = df.sort_values(by="date", ascending=True)
            df = df.groupby([pd.Grouper(key='date', freq='ME')],
                            as_index=False)["probability"].sum()

            plt.plot(df["date"],
                     df["probability"],
                     color=plot_colors[topic_id % len(plot_colors)])
        return fig




