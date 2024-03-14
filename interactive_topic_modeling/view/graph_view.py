import matplotlib.pyplot as plt
from PySide6.QtWidgets import QWidget, QTabWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import (FigureCanvasQTAgg as
                                                FigureCanvas)
from matplotlib.ticker import MaxNLocator
from wordcloud import WordCloud

from interactive_topic_modeling.backend.model.abstract_model import TermLists
from interactive_topic_modeling.backend.model.lda_model import GensimLdaModel
from interactive_topic_modeling.backend.preprocessing.pipeline import Pipeline
from interactive_topic_modeling.view.topic_view.fetched_topics_display \
    import FetchedTopicsDisplay


class GraphView(QTabWidget):
    """A class for displaying the graphs made by topic modelling"""
    num_topics = 0

    def __init__(self) -> None:
        """Initialize the GraphDisplay."""
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
        active_tab_name = self.tabText(self.currentIndex())

        # Perform LDA with additional stopwords exclusion
        lda_model = self.perform_lda_on_docs(active_tab_name, corpus,
                                             additional_stopwords)

        # Add LDA plots to active tab
        self.add_lda_plots(active_tab_name, lda_model)

        # Event handling
        self.tabBarClicked.connect(self.on_tab_clicked)

        self.display_plot(active_tab_name, 0)

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
        self.fetched_topics_display.clear_topics()

        # Add topics to fetched topics view
        for i in range(self.num_topics):
            topic_name = f"Topic {i + 1}"
            topic_words = lda_model.show_topic_terms(i, 10)
            cleaned_topic_words = [word for word, _ in topic_words]
            self.fetched_topics_display.add_topic(tab_name, topic_name,
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
        Add LDA plots for the given LDA model.

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

    def construct_word_clouds(self, lda_model: GensimLdaModel):
        """
        Construct word cloud plots for the given LDA model.

        :param lda_model: The LDA model to construct the plots for
        :return: A list of word cloud plots
        """
        canvases = []

        for i in range(self.num_topics):
            wordcloud = (WordCloud(width=800,
                                   height=400,
                                   background_color='white'))

            wordcloud.generate_from_frequencies(
                    dict(lda_model.show_topic(i, 30))
            )

            # Construct a word cloud
            fig = plt.figure()
            plt.imshow(wordcloud, interpolation='bilinear')
            plt.axis('off')
            plt.tight_layout(pad=0)

            canvases.append(FigureCanvas(fig))

        return canvases

    def construct_probable_words(self, lda_model: GensimLdaModel) -> (
            list)[FigureCanvas]:
        """
        Construct bar plots for the words with the highest probability for
        the given LDA model.

        :param lda_model: The LDA model to construct the plots for
        :return: A list of probable words plots
        """
        canvases = []

        for i in range(self.num_topics):
            topic_words, topic_weights = lda_model.show_topic_and_probs(i,
                                                                        10)

            # Construct a bar plot
            fig = plt.figure()
            plt.bar(topic_words, topic_weights, color="darkblue")

            # Add margins and labels to the plot
            plt.margins(0.02)
            plt.ylabel("gewicht")
            plt.title("Woorden met het hoogste gewicht topic {}".format(i))

            canvases.append(FigureCanvas(fig))

        return canvases

    def construct_correlation_matrix(self,
                                     lda_model:
                                     GensimLdaModel) -> FigureCanvas:
        """
        Construct the correlation matrix. 
        
        :param lda_model: The trained LDA model.
        :return FigureCanvas: The graph showing the correlation matrix
        """
        # Construct the correlation matrix
        correlation_matrix = lda_model.get_correlation_matrix(num_words=30)

        # Construct a plot and axeschat
        fig, ax = plt.subplots()

        # Construct the correlations matrix adding colors
        data = ax.imshow(correlation_matrix, cmap='RdBu_r', origin='lower')

        # Add a color bar to the plot
        plt.colorbar(data)

        # Add a title and correct integer ticks on both axes
        plt.title("Correlatiematrix topics")
        fig.gca().yaxis.set_major_locator(MaxNLocator(integer=True))
        fig.gca().xaxis.set_major_locator(MaxNLocator(integer=True))

        return FigureCanvas(fig)

    def get_active_tab_name(self) -> str:
        """
        Get the name of the active tab.

        :return: The name of the active tab
        """
        return self.tabText(self.currentIndex())

    def display_plot(self, tab_name: str, plot_index: int) -> None:
        """
        Display the plots for the given tab.

        :param plot_index: Index of the plot to view
        :param tab_name: Name of the tab to view the plots for
        :return: None
        """
        # Clear the layout
        for i in reversed(range(self.init_model_layout.count())):
            self.init_model_layout.itemAt(i).widget().setParent(None)

        # Check if plot index is valid
        if plot_index < 0 or plot_index >= len(self.plots_container[tab_name]):
            return

        # Add the plot to the layout
        self.init_model_layout.addWidget(
                self.plots_container[tab_name][plot_index])

    def on_tab_clicked(self, index) -> None:
        """
        Event handler for when a tab is clicked.

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
        Display the next plot for the given tab.

        :param tab_name: Name of the tab to view the next plot for
        :return: None
        """

        if tab_name not in self.plots_container:
            return

        self.plot_index[tab_name] = (self.plot_index[tab_name] + 1) % len(
                self.plots_container[tab_name])
        self.display_plot(tab_name, self.plot_index[tab_name])

    def previous_plot(self, tab_name: str) -> None:
        """
        Display the previous plot for the given tab.

        :param tab_name: Name of the tab to view the previous plot for
        :return: None
        """

        if tab_name not in self.plots_container:
            return

        self.plot_index[tab_name] = (self.plot_index[tab_name] - 1) % len(
                self.plots_container[tab_name])
        self.display_plot(tab_name, self.plot_index[tab_name])


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University 
(Department of Information and Computing Sciences)
"""
