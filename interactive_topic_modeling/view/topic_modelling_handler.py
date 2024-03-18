import random
import matplotlib.figure
import networkx as nx

from matplotlib import pyplot as plt
from matplotlib.backends.backend_template import FigureCanvas
from matplotlib.ticker import MaxNLocator
from wordcloud import WordCloud

from interactive_topic_modeling.backend.model.abstract_model import TermLists
from interactive_topic_modeling.backend.model.lda_model import GensimLdaModel
from interactive_topic_modeling.backend.preprocessing.pipeline import Pipeline
from interactive_topic_modeling.view.graph_view import GraphView
from interactive_topic_modeling.view.model_selection_view import \
    ModelSelectionView
from interactive_topic_modeling.view.topic_view.fetched_topics_view import \
    FetchedTopicsView


def generate_list():
    # Define the range of numbers
    low_range = 1
    high_range = 10050

    # Define the desired length of the list
    list_length = 1000

    # Generate a list of random numbers
    random_list = [random.randint(low_range, high_range) for _ in
                   range(list_length)]

    return random_list


class TopicModellingHandler:
    """Dummy class handling topic modelling in the frontend."""

    def __init__(self,
                 model: ModelSelectionView,
                 graph: GraphView,
                 fetched_topics: FetchedTopicsView) -> None:
        self.num_topics = 5
        self.model_selection_view = model
        self.graph_view = graph
        self.fetched_topics_view = fetched_topics

        # { tab_name, lda_model }
        self.lda_model_container = {}

        # { tab_name, [canvas] }
        # TODO: Added NMF model for demo purposes, remove later
        self.plots_container = {"nmf_model": [FigureCanvas()]}

        # { tab_name, plot_index }
        self.plot_index = {}

    def apply_topic_modelling(self, corpus: list, topic_amount: int,
                              additional_stopwords: set) -> None:
        """
        Apply topic modelling to the given corpus.

        :param corpus: The corpus to apply topic modelling to
        :param topic_amount: The amount of topics to generate
        :param additional_stopwords: The set of additional stopwords to
                                     exclude during topic modeling
        :return: None
        """

        # Set number of topics
        self.num_topics = topic_amount

        # Get active tab name
        active_tab_name = self.model_selection_view.get_active_tab_name()

        # Perform LDA with additional stopwords exclusion
        lda_model = self.perform_lda_on_docs(active_tab_name, corpus,
                                             additional_stopwords)

        # Add LDA plots to active tab
        self.add_lda_plots(active_tab_name, lda_model)
        self.graph_view.display_plot(
            self.plots_container[active_tab_name][0])

    def perform_lda_on_docs(self, tab_name: str, documents: list,
                            additional_stopwords: set[str]) -> GensimLdaModel:
        """
        Perform LDA on the given text.

        :param tab_name: Name of the tab to perform LDA on
        :param documents: The documents to perform LDA on
        :param additional_stopwords: The set of additional stopwords
                                     to exclude during LDA
        :return: The trained LDA model
        """
        # Get text from documents
        text_from_docs = [document.body for document in documents]

        # Preprocess documents with additional stopwords exclusion
        # TODO: real preprocessing
        pipe = Pipeline()
        pipe.add_stopwords(additional_stopwords)
        tokens = [pipe(doc_text) for doc_text in text_from_docs]

        # Train LDA model
        lda_model = self.train_lda_model(tokens)

        # Save LDA model
        self.lda_model_container[tab_name] = lda_model

        # Clear fetched topics view
        self.fetched_topics_view.clear_topics()

        # Add topics to fetched topics view
        for i in range(self.num_topics):
            topic_name = f"Topic {i + 1}"
            topic_words = lda_model.show_topic_terms(i, 10)
            cleaned_topic_words = [word for word, _ in topic_words]
            self.fetched_topics_view.add_topic(tab_name, topic_name,
                                               cleaned_topic_words)

        return lda_model

    def train_lda_model(self, corpus: TermLists) -> GensimLdaModel:
        """
        Train an LDA model.

        :param corpus: The corpus to train the LDA model on
        :return: The trained LDA model
        """
        lda_model = GensimLdaModel(corpus, self.num_topics)
        return lda_model

    def add_lda_plots(self, tab_name: str, lda_model: GensimLdaModel) -> None:
        """
        Add LDA plots for the given LDA model
        :param tab_name: Name of the tab to add the plots to
        :param lda_model: The LDA model to add the plots for
        :return: None
        """
        canvases = []
        canvases.extend(self.construct_word_clouds(lda_model))
        canvases.extend(self.construct_probable_words(lda_model))
        canvases.append(self.construct_correlation_matrix(lda_model))
        canvases.append(self.construct_word_topic_network_vis(lda_model))
        # canvases.append(self.construct_word_count())

        self.plots_container[tab_name] = canvases
        self.plot_index[tab_name] = 0

    def construct_word_clouds(self, lda_model: GensimLdaModel) \
            -> list[matplotlib.figure.Figure]:
        """
        Construct word cloud plots for the given LDA model

        :param lda_model: The LDA model to construct the plots for
        :return: A list of word cloud plots
        """
        canvases = []

        for i in range(self.num_topics):
            wordcloud = (WordCloud(width=800, height=400,
                                   background_color='white').
            generate_from_frequencies(
                dict(lda_model.show_topic(i, 30))
            ))

            # Construct a word cloud
            fig = plt.figure()
            plt.imshow(wordcloud, interpolation='bilinear')
            plt.axis('off')
            plt.tight_layout(pad=0)

            canvases.append(fig)

        return canvases

    def construct_probable_words(self, lda_model: GensimLdaModel) \
            -> list[matplotlib.figure.Figure]:
        """
        Construct probable words plots for the given LDA model

        :param lda_model: The LDA model to construct the plots for
        :return: A list of probable words plots
        """
        canvases = []

        for i in range(self.num_topics):
            topic_words, topic_weights = lda_model.show_topic_and_probs(i, 15)

            # Construct a horizontal bar plot
            fig = plt.figure()
            plt.barh(topic_words, topic_weights, color="darkblue")
            plt.gca().invert_yaxis()

            # Add margins and labels to the plot
            plt.margins(0.02)
            plt.ylabel("gewicht")
            plt.title("Woorden met het hoogste gewicht topic {}".format(i + 1))

            canvases.append(FigureCanvas(fig))

        return canvases

    def construct_word_count(self) -> matplotlib.figure.Figure:
        """
        Construct a word count plot

        :return: A word count plot
        """
        document_counts = generate_list()

        # Construct a histogram
        fig = plt.figure()
        plt.hist(document_counts, bins=150, color="darkblue")

        # Add margins and labels to the plot
        plt.margins(x=0.02)
        plt.xlabel("aantal woorden per document")
        plt.ylabel("aantal documenten")
        plt.title("Distributie aantal woorden per document")

        return fig

    def construct_correlation_matrix(self,
                                     lda_model: GensimLdaModel) \
            -> matplotlib.figure.Figure:
        """
        Construct a correlation matrix plot for the given LDA model

        :param lda_model: The LDA model to construct the plot for
        :return: A correlation matrix plot
        """
        # Construct the correlation matrix
        correlation_matrix = lda_model.get_correlation_matrix(num_words=30)

        # Construct a plot and axes
        fig, ax = plt.subplots()

        # Construct the correlations matrix adding colors
        data = ax.imshow(correlation_matrix, cmap='RdBu_r', origin='lower')

        # Add a color bar to the plot
        plt.colorbar(data)

        # Add a title and correct integer ticks on both axes
        plt.title("Correlatiematrix topics")
        fig.gca().yaxis.set_major_locator(MaxNLocator(integer=True))
        fig.gca().xaxis.set_major_locator(MaxNLocator(integer=True))

        return fig

    def construct_word_topic_network_vis(self,
                                         lda_model: GensimLdaModel) \
            -> FigureCanvas:
        """
        Construct a word-topic network plot for the given LDA model

        :param lda_model: The LDA model to construct the plot for
        :return: A word-topic network plot
        """
        # Construct a plot and graph
        fig = plt.figure()
        graph = self.construct_word_topic_network(lda_model)

        # Get the scale factor used for the displayed edge weight (width)
        edge_scale_factor = self.get_edge_scale_factor(lda_model)

        # Get graph elements
        edges = graph.edges()
        nodes = graph.nodes(data="color")

        # Get drawing function arguments
        node_sizes = [150 if node[1] is not None else 0 for node in nodes]
        node_colors = [node[1] if node[1] is not None else "black" for node in
                       nodes]

        edge_colors = [graph[u][v]["color"] for (u, v) in edges]
        edge_width = [(graph[u][v]["weight"] * edge_scale_factor) for u, v in
                      edges]

        # Draw the graph
        nx.draw_kamada_kawai(graph,
                             node_size=node_sizes,
                             with_labels=True,
                             width=edge_width,
                             edge_color=edge_colors,
                             node_color=node_colors,
                             font_size=8)

        return FigureCanvas(fig)

    def construct_word_topic_network(self,
                                     lda_model: GensimLdaModel) -> nx.Graph:
        """
        Construct a word-topic network for the given LDA model

        :param lda_model: The LDA model to construct the network for
        :return: A networkx graph
        """
        graph = nx.Graph()

        # Define colors for the topics
        colors = ['#e6194b', '#3cb44b', '#ffe119', '#4363d8', '#f58231',
                  '#9a6324', '#46f0f0', '#f032e6', '#bcf60c',
                  '#fabebe', '#008080', '#e6beff', '#000075', '#fffac8',
                  '#800000', '#aaffc3', '#808000', '#ffd8b1',
                  '#808080', '#911eb4']

        # Amount of words displayed for each topic
        node_amount = 15

        for topic_id in range(self.num_topics):
            topic_tuples = lda_model.show_topic(topic_id, node_amount)
            for topic_tuple in topic_tuples:
                graph.add_node(topic_id + 1, color=colors[topic_id % 20])
                graph.add_edge(topic_id + 1, topic_tuple[0],
                               color=colors[topic_id % 20],
                               weight=topic_tuple[1])
        return graph

    def get_edge_scale_factor(self, lda_model: GensimLdaModel) -> float:
        """
        Get the edge scale factor for the given LDA model

        :param lda_model: The LDA model to calculate the scale factor for
        :return: The edge scale factor
        """

        # Find the maximum topic weight
        max_topic_weight = 0
        for topic_id in range(self.num_topics):
            _, topic_weights = lda_model.show_topic_and_probs(topic_id, 1)
            max_topic_weight = max(max_topic_weight, topic_weights[0])

        # Choose a weight to display
        chosen_weight = 1.5

        scale_factor = (1 / max_topic_weight)

        return scale_factor * chosen_weight


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University 
(Department of Information and Computing Sciences)
"""
