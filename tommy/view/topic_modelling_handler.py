import random
import matplotlib.figure

from matplotlib import pyplot as plt
from matplotlib.backends.backend_template import FigureCanvas
from matplotlib.ticker import MaxNLocator
from wordcloud import WordCloud

from tommy.backend.model.abstract_model import TermLists
from tommy.backend.model.lda_model import GensimLdaModel
from tommy.backend.preprocessing.pipeline import Pipeline
from tommy.controller.corpus_controller import CorpusController
from tommy.view.graph_view import GraphView
from tommy.view.model_selection_view import \
    ModelSelectionView
from tommy.view.topic_view.fetched_topics_view import \
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
        # text_from_docs = [document.body for document in documents]
        text_from_docs = CorpusController.get_raw_bodies()

        # Preprocess documents with additional stopwords exclusion
        # TODO: real preprocessing
        pipe = Pipeline()
        pipe.add_stopwords(additional_stopwords)
        tokens = [pipe(doc_text.body) for doc_text in text_from_docs]

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

            canvases.append(FigureCanvas(fig))

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
            topic_words, topic_weights = lda_model.show_topic_and_probs(i, 10)

            # Construct a bar plot
            fig = plt.figure()
            plt.bar(topic_words, topic_weights, color="darkblue")

            # Add margins and labels to the plot
            plt.margins(0.02)
            plt.ylabel("gewicht")
            plt.title("Woorden met het hoogste gewicht topic {}".format(i))

            canvases.append(fig)

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


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University 
(Department of Information and Computing Sciences)
"""
