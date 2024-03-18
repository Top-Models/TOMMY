import numpy as np
from PySide6.QtWidgets import QWidget, QTabWidget, QVBoxLayout, QPushButton
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from wordcloud import WordCloud
from gensim import corpora, models
import random
import networkx as nx

from interactive_topic_modeling.backend.model.abstract_model import TermLists
from interactive_topic_modeling.backend.model.lda_model import GensimLdaModel
from interactive_topic_modeling.backend.preprocessing.pipeline import Pipeline
# Assuming you have this import statement
from interactive_topic_modeling.display.topic_display.fetched_topics_display import FetchedTopicsDisplay


def preprocess_text(text) -> list:
    tokens = text.lower().split()
    return tokens


def perform_lda_on_text(text, num_topics):
    # Preprocess the text
    preprocessed_text = preprocess_text(text)

    # Create a dictionary from the preprocessed text
    dictionary = corpora.Dictionary([preprocessed_text])

    # Create a bag-of-words representation of the corpus
    corpus = [dictionary.doc2bow(preprocessed_text)]

    # Train the LDA model
    lda_model = models.LdaModel(corpus, num_topics=num_topics, id2word=dictionary, passes=10)

    return lda_model


def generate_list():
    # Define the range of numbers
    low_range = 1
    high_range = 10050

    # Define the desired length of the list
    list_length = 1000

    # Generate a list of random numbers
    random_list = [random.randint(low_range, high_range) for _ in range(list_length)]

    return random_list


class GraphDisplay(QTabWidget):
    num_topics = 0

    def __init__(self):
        super().__init__()

        # Initialize widget properties
        self.setStyleSheet("""        
                QTabWidget {
                    color: black;
                    border: none;
                }

                QTabWidget::pane {
                    border: none;
                }

                QTabBar::tab { 
                    background-color: #FFFFFF; 
                    color: gray;
                    font-size: 15px;
                    padding: 7px;
                    font-weight: bold;
                }

                QTabBar::tab:selected {
                    border-bottom: 2px solid #E40046;
                    color: #000000;
                }

                QTabBar::tab:hover {
                    color: #000000;
                }                
            """)

        # { tab_name, lda_model }
        self.lda_model_container = {}

        # { tab_name, [canvas] }
        self.plots_container = {}

        # { tab_name, plot_index }
        self.plot_index = {}

        # Initialize widgets
        self.fetched_topics_display = FetchedTopicsDisplay()

        # Add first tab
        self.lda_model = QWidget()
        self.init_model_layout = QVBoxLayout()
        self.lda_model.setLayout(self.init_model_layout)
        self.addTab(self.lda_model, "lda_model")

    def apply_topic_modelling(self, corpus: list, topic_amount: int, additional_stopwords: set) -> None:
        """
        Apply topic modelling to the given corpus
        :param corpus: The corpus to apply topic modelling to
        :param topic_amount: The amount of topics to generate
        :param additional_stopwords: The set of addtional stopwords to exclude during topic modeling
        :return: None
        """

        # Set number of topics
        self.num_topics = topic_amount
        # Get active tab name
        active_tab_name = self.tabText(self.currentIndex())

        # Perform LDA with additional stopwords exclusion
        lda_model = self.perform_lda_on_docs(active_tab_name, corpus, additional_stopwords)

        # Add LDA plots to active tab
        self.add_lda_plots(active_tab_name, lda_model)

        # Event handling
        self.tabBarClicked.connect(self.on_tab_clicked)

        self.display_plot(active_tab_name, 0)

    def preprocess_text(self, text, additional_stopwords: set) -> list:
        tokens = text.lower().split()
        # Exclude stopwords
        tokens = [token for token in tokens if token not in additional_stopwords]
        return tokens

    def perform_lda_on_docs(self, tab_name: str, documents: list, additional_stopwords: set[str]) -> GensimLdaModel:
        """
        Perform LDA on the given text
        :param tab_name: Name of the tab to perform LDA on
        :param documents: The documents to perform LDA on
        :param additional_stopwords: The set of additional stopwords to exclude during LDA
        :return: The trained LDA model
        """
        # Get text from documents
        text_from_docs = [document.body for document in documents]

        # Preprocess documents with additional stopwords exclusion
        # TODO: real preprocessing
        pipe = Pipeline()
        #print(additional_stopwords)
        pipe.add_stopwords(additional_stopwords)
        tokens = [pipe(doc_text) for doc_text in text_from_docs]

        # Train LDA model
        lda_model = self.train_lda_model(tokens)

        # Save LDA model
        self.lda_model_container[tab_name] = lda_model

        # Clear fetched topics display
        self.fetched_topics_display.clear_topics()

        # Add topics to fetched topics display
        for i in range(self.num_topics):
            topic_name = f"Topic {i + 1}"
            topic_words = lda_model.show_topic_terms(i, 10)
            cleaned_topic_words = [word for word, _ in topic_words]
            self.fetched_topics_display.add_topic(tab_name, topic_name, cleaned_topic_words)

        return lda_model

    def train_lda_model(self, corpus: TermLists) -> GensimLdaModel:
        """
        Train an LDA model
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

    def construct_word_clouds(self, lda_model: GensimLdaModel):
        """
        Construct word cloud plots for the given LDA model
        :param lda_model: The LDA model to construct the plots for
        :return: A list of word cloud plots
        """
        canvases = []

        for i in range(self.num_topics):
            wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(
                dict(lda_model.show_topic(i, 30))
            )

            # Construct a word cloud
            fig = plt.figure()
            plt.imshow(wordcloud, interpolation='bilinear')
            plt.axis('off')
            plt.tight_layout(pad=0)
            plt.title("Woordenwolk topic {}".format(i+1))

            canvases.append(FigureCanvas(fig))

        return canvases

    def construct_probable_words(self, lda_model: GensimLdaModel) -> list[FigureCanvas]:
        """
        Construct bar plots for the words with the highest probability for the given LDA model
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
            plt.title("Woorden met het hoogste gewicht topic {}".format(i+1))

            canvases.append(FigureCanvas(fig))

        return canvases

    def construct_word_count(self) -> FigureCanvas:
        """
        Construct a histogram containing word counts of each input document for the given LDA model
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

        return FigureCanvas(fig)

    def construct_correlation_matrix(self, lda_model: GensimLdaModel) -> FigureCanvas:
        # Construct the correlation matrix
        correlation_matrix = lda_model.get_correlation_matrix(num_words=30)
        adjusted_matrix = np.pad(correlation_matrix, ((1, 0), (1, 0)), mode='constant')


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

        # Adjust the plot ticks so that they start from 1 instead of 0
        plt.xticks(np.arange(self.num_topics), np.arange(1, self.num_topics+1))
        plt.yticks(np.arange(self.num_topics), np.arange(1, self.num_topics + 1))

        return FigureCanvas(fig)

    def construct_word_topic_network_vis(self, lda_model: GensimLdaModel) -> FigureCanvas:
        """
        Construct a word-topic network plot showing the relations between topics and probable words
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
        node_colors = [node[1] if node[1] is not None else "black" for node in nodes]

        edge_colors = [graph[u][v]["color"] for (u, v) in edges]
        edge_width = [(graph[u][v]["weight"] * edge_scale_factor) for u, v in edges]

        # Draw the network using the kamada-kawai algorithm to position the nodes in an aesthetically pleasing way
        nx.draw_kamada_kawai(graph,
                             node_size=node_sizes,
                             with_labels=True,
                             width=edge_width,
                             edge_color=edge_colors,
                             node_color=node_colors,
                             font_size=8)

        return FigureCanvas(fig)

    def construct_word_topic_network(self, lda_model: GensimLdaModel) -> nx.Graph:
        """"
        Construct a word-topic network which is used to plot the relations between topics and probable words
        :param lda_model: The LDA model to construct the network for
        :return: A networkx graph
        """
        graph = nx.Graph()

        # List of simple, distinct colors from https://sashamaps.net/docs/resources/20-colors/
        colors = ['#e6194b', '#3cb44b', '#ffe119', '#4363d8', '#f58231', '#9a6324', '#46f0f0', '#f032e6', '#bcf60c',
                  '#fabebe', '#008080', '#e6beff', '#000075', '#fffac8', '#800000', '#aaffc3', '#808000', '#ffd8b1',
                  '#808080', '#911eb4']

        # Amount of words displayed for each topic
        node_amount = 15

        for topic_id in range(self.num_topics):
            topic_tuples = lda_model.show_topic(topic_id, node_amount)
            for topic_tuple in topic_tuples:
                graph.add_node(topic_id, color=colors[topic_id % 20])
                graph.add_edge(topic_id, topic_tuple[0], color=colors[topic_id % 20], weight=topic_tuple[1])
        return graph

    def get_edge_scale_factor(self, lda_model: GensimLdaModel) -> float:
        """
        Calculates the scale factor to make sure the biggest edge in a network is always the same size, regardless of
        the maximum topic weight
        :param lda_model: The LDA model to calculate the scale factor for
        :return: The edge scale factor
        """

        # Find the maximum topic weight
        max_topic_weight = 0
        for topic_id in range(self.num_topics):
            _, topic_weights = lda_model.show_topic_and_probs(topic_id, 1)
            max_topic_weight = max(max_topic_weight, topic_weights[0])

        # A constant which is multiplied by the scale factor according to an edge width that is visually pleasing
        chosen_weight = 1.5

        scale_factor = (1 / max_topic_weight)

        return scale_factor * chosen_weight

    def get_active_tab_name(self) -> str:
        """
        Get the name of the active tab
        :return: The name of the active tab
        """
        return self.tabText(self.currentIndex())

    def display_plot(self, tab_name: str, plot_index: int) -> None:
        """
        Display the plots for the given tab
        :param plot_index: Index of the plot to display
        :param tab_name: Name of the tab to display the plots for
        :return: None
        """

        # Clear the layout
        for i in reversed(range(self.init_model_layout.count())):
            self.init_model_layout.itemAt(i).widget().setParent(None)

        # Check if plot index is valid
        if plot_index < 0 or plot_index >= len(self.plots_container[tab_name]):
            return

        # Add the plot to the layout
        self.init_model_layout.addWidget(self.plots_container[tab_name][plot_index])

    def on_tab_clicked(self, index) -> None:
        """
        Event handler for when a tab is clicked
        :param index: Index of the clicked tab
        :return: None
        """
        clicked_tab_name = self.tabText(index)
        self.fetched_topics_display.display_topics(clicked_tab_name)

        if clicked_tab_name not in self.plots_container:
            return

        self.display_plot(clicked_tab_name, self.plot_index[clicked_tab_name])

    def next_plot(self, tab_name: str) -> None:
        """
        Display the next plot for the given tab
        :param tab_name: Name of the tab to display the next plot for
        :return: None
        """

        if tab_name not in self.plots_container:
            return

        self.plot_index[tab_name] = (self.plot_index[tab_name] + 1) % len(self.plots_container[tab_name])
        self.display_plot(tab_name, self.plot_index[tab_name])

    def previous_plot(self, tab_name: str) -> None:
        """
        Display the previous plot for the given tab
        :param tab_name: Name of the tab to display the previous plot for
        :return: None
        """

        if tab_name not in self.plots_container:
            return

        self.plot_index[tab_name] = (self.plot_index[tab_name] - 1) % len(self.plots_container[tab_name])
        self.display_plot(tab_name, self.plot_index[tab_name])
