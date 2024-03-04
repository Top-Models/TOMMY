from PySide6.QtWidgets import QWidget, QTabWidget, QVBoxLayout, QPushButton
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from gensim import corpora, models

from interactive_topic_modeling.backend.model.abstract_model import TermLists
from interactive_topic_modeling.backend.model.lda_model import GensimLdaModel
# Assuming you have this import statement
from interactive_topic_modeling.display.topic_display.fetched_topics_display import FetchedTopicsDisplay


def preprocess_text(text) -> list:
    tokens = text.lower().split()
    return tokens


class GraphDisplay(QTabWidget):
    num_topics = 5

    def __init__(self):
        super().__init__()

        # Initialize widget properties
        self.setStyleSheet("""        
                QTabWidget {
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
        self.init_model = QWidget()
        self.init_model_layout = QVBoxLayout()
        self.init_model.setLayout(self.init_model_layout)
        self.addTab(self.init_model, "lda_model")

        self.sample_text = """
        In de weelderige bamboebossen van China, waar de lucht dik is van de mist en fluisteringen van oude verhalen, zwerft de geliefde reuzenpanda, een wezen zowel charmant als raadselachtig.

Met zijn iconische zwart-witte vacht die lijkt op een formeel pak, is de panda de VIP van de natuur, klaar om elke rode loper te betreden met zijn schattige aanwezigheid. Maar laat je niet misleiden door zijn chique kledij; achter die betoverende ogen schuilt een speelse geest en een hart zo groot als zijn knuffelige gestalte.

Panda's zijn het toonbeeld van zenmeesters, die hun dagen lui doorbrengen met het knabbelen op bamboescheuten, hun favoriete lekkernij. Terwijl ze lui tegen de stam van een boom leunen, hun pluizige buikjes vol, lijken ze een aura van rust uit te stralen die zelfs de meest rusteloze zielen kalmeert.

Maar laat je niet misleiden door hun relaxte houding; panda's zijn bedreven klimmers en kunnen snel de hoogste bomen beklimmen met de gratie van een ninja. Met een ondeugende glinstering in hun ogen voeren ze acrobatische toeren uit die elke circusartiest te schande zouden maken, allemaal in de jacht op de sappigste bamboescheuten.

En laten we de pandawelpen niet vergeten, de kleine balletjes van bont die de show stelen met hun klunzige capriolen en hartverwarmende piepjes. Terwijl ze tuimelen en rollen in een speelse razernij, is het onmogelijk om niet te glimlachen om hun schattige onhandigheid.

In een wereld vol chaos en onzekerheid herinneren panda's ons eraan om te vertragen, te genieten van de eenvoudige geneugten en onze speelse kant te omarmen. Dus de volgende keer dat je je gestrest of overweldigd voelt, neem dan een voorbeeld aan de panda's en geniet van een moment van ontspanning, panda-stijl. Immers, het leven is te kort om te serieus te nemen als er bamboescheuten te knabbelen en bomen te beklimmen zijn!
        """

        # Get active tab name
        active_tab_name = self.tabText(self.currentIndex())

        # Perform LDA
        lda_model = self.perform_lda_on_text(active_tab_name, self.sample_text)

        # Add LDA plots to active tab
        self.add_lda_plots(active_tab_name, lda_model)

        # Event handling
        self.tabBarClicked.connect(self.on_tab_clicked)

        self.display_plot(active_tab_name, 0)

    def perform_lda_on_text(self, tab_name: str, text: str) -> GensimLdaModel:
        """
        Perform LDA on the given text
        :param tab_name: Name of the tab to perform LDA on
        :param text: The text to perform LDA on
        :return: The trained LDA model
        """
        # Preprocess text
        tokens = preprocess_text(text)

        # TODO: Create list of lists of tokens with with multiple documents

        # Train LDA model
        lda_model = self.train_lda_model([tokens])

        # Save LDA model
        self.lda_model_container[tab_name] = lda_model

        return lda_model

    def train_lda_model(self, corpus: TermLists) -> GensimLdaModel:
        """
        Train an LDA model
        :param dictionary: The dictionary to train the model on
        :return: The trained LDA model
        """
        lda_model = GensimLdaModel(corpus, self.num_topics)
        return lda_model

    def add_lda_plots(self, tab_name: str, lda_model: GensimLdaModel) -> None:
        """
        Add a word cloud plot for the given LDA model
        :param tab_name: Name of the tab to add the plot to
        :param lda_model: The LDA model to add a plot for
        :return: None
        """
        canvases = self.construct_wordclouds(tab_name, lda_model)
        self.plots_container[tab_name] = canvases
        self.plot_index[tab_name] = 0

    def construct_wordclouds(self, tab_name: str, lda_model: GensimLdaModel):
        """
        Construct word cloud plots for the given LDA model
        :param tab_name: Name of the tab to construct the plots for
        :param lda_model: The LDA model to construct the plots for
        :return: A list of word cloud plots
        """
        canvases = []

        for i in range(self.num_topics):
            wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(
                dict(lda_model.model.show_topic(i, topn=30))
            )

            canvas = FigureCanvas(plt.figure())
            plt.imshow(wordcloud, interpolation='bilinear')
            plt.axis('off')
            plt.tight_layout(pad=0)
            canvases.append(canvas)

        return canvases

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
