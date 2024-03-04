import numpy as np
from PySide6.QtWidgets import QWidget, QTabWidget, QVBoxLayout, QPushButton
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from gensim import corpora, models
import random

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
        self.addTab(self.init_model, "init_model")

        self.sample_text = """
        In de weelderige bamboebossen van China, waar de lucht dik is van de mist en fluisteringen van oude verhalen, zwerft de geliefde reuzenpanda, een wezen zowel charmant als raadselachtig.

Met zijn iconische zwart-witte vacht die lijkt op een formeel pak, is de panda de VIP van de natuur, klaar om elke rode loper te betreden met zijn schattige aanwezigheid. Maar laat je niet misleiden door zijn chique kledij; achter die betoverende ogen schuilt een speelse geest en een hart zo groot als zijn knuffelige gestalte.

Panda's zijn het toonbeeld van zenmeesters, die hun dagen lui doorbrengen met het knabbelen op bamboescheuten, hun favoriete lekkernij. Terwijl ze lui tegen de stam van een boom leunen, hun pluizige buikjes vol, lijken ze een aura van rust uit te stralen die zelfs de meest rusteloze zielen kalmeert.

Maar laat je niet misleiden door hun relaxte houding; panda's zijn bedreven klimmers en kunnen snel de hoogste bomen beklimmen met de gratie van een ninja. Met een ondeugende glinstering in hun ogen voeren ze acrobatische toeren uit die elke circusartiest te schande zouden maken, allemaal in de jacht op de sappigste bamboescheuten.

En laten we de pandawelpen niet vergeten, de kleine balletjes van bont die de show stelen met hun klunzige capriolen en hartverwarmende piepjes. Terwijl ze tuimelen en rollen in een speelse razernij, is het onmogelijk om niet te glimlachen om hun schattige onhandigheid.

In een wereld vol chaos en onzekerheid herinneren panda's ons eraan om te vertragen, te genieten van de eenvoudige geneugten en onze speelse kant te omarmen. Dus de volgende keer dat je je gestrest of overweldigd voelt, neem dan een voorbeeld aan de panda's en geniet van een moment van ontspanning, panda-stijl. Immers, het leven is te kort om te serieus te nemen als er bamboescheuten te knabbelen en bomen te beklimmen zijn!
        """

        # Add second tab (for demonstration)
        self.demo_second_tab = QWidget()
        self.demo_second_tab.setStyleSheet("background-color: pink;")
        self.addTab(self.demo_second_tab, "demo_second_tab")

        # Perform LDA
        lda_model = perform_lda_on_text(self.sample_text, self.num_topics)

        # Get active tab name
        active_tab_name = self.tabText(self.currentIndex())

        # Add LDA plots to active tab
        self.add_lda_plots(active_tab_name, lda_model)

        # Event handling
        self.tabBarClicked.connect(self.on_tab_clicked)

        self.display_plot(active_tab_name, 0)

    def add_lda_plots(self, tab_name: str, lda_model) -> None:
        """
        Add word cloud plots for the given LDA model
        :param tab_name: Name of the tab to add the plots to
        :param lda_model: The LDA model to add the plots for
        :return: None
        """
        plots = []
        self.plot_index[tab_name] = 0
        self.plots_container[tab_name] = []

        plots.extend(self.construct_wordclouds(lda_model))
        plots.append(self.construct_word_count())
        plots.extend(self.construct_common_words(lda_model))
        plots.append(self.construct_correlation_matrix(lda_model))

        for plot in plots:
            self.plots_container[tab_name].append(plot)

    def construct_wordclouds(self, lda_model) -> list[FigureCanvas]:
        canvases = []
        for topic_id, topic in enumerate(lda_model.print_topics(num_topics=self.num_topics, num_words=20)):
            topic_words = " ".join([word.split("*")[1].strip() for word in topic[1].split(" + ")])

            wordcloud = WordCloud(width=800, height=800, random_state=15, max_font_size=110).generate(topic_words)

            # Create a Matplotlib figure and canvas
            fig, ax = plt.subplots()
            ax.imshow(wordcloud, interpolation="bilinear")
            ax.axis("off")
            ax.set_title("Topic: {}".format(topic_id))

            canvases.append(FigureCanvas(fig))
        return canvases


    def construct_common_words(self, lda_model) -> list[FigureCanvas]:
        canvases = []
        for topic_id, topic in enumerate(lda_model.print_topics(num_topics=self.num_topics, num_words=10)):
            topic_words = [word.split("*")[1].strip() for word in topic[1].split(" + ")]
            topic_weights = [float(word.split("*")[0].strip()) for word in topic[1].split(" + ")]

            fig = plt.figure()
            plt.bar(topic_words, topic_weights, color="darkblue")

            plt.margins(0.02)
            plt.ylabel("gewicht")
            plt.title("Meest voorkomende woorden topic {}".format(topic_id))

            canvases.append(FigureCanvas(fig))

        return canvases

    def construct_word_count(self) -> FigureCanvas:
        document_counts = generate_list()

        fig = plt.figure()
        plt.hist(document_counts, bins=150, color="darkblue")

        plt.margins(x=0.02)
        plt.xlabel("aantal woorden per document")
        plt.ylabel("aantal documenten")
        plt.title("Distributie aantal woorden per document")

        return FigureCanvas(fig)

    def construct_correlation_matrix(self, lda_model) -> FigureCanvas:
        difference_matrix, annotation = lda_model.diff(lda_model, distance='jaccard', num_words=20, annotation=False)

        fig, ax = plt.subplots()
        data = ax.imshow(difference_matrix, cmap='RdBu_r', origin='lower')
        plt.colorbar(data)
        plt.title("Correlatiematrix topics")
        return FigureCanvas(fig)

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
        self.display_plot(clicked_tab_name, self.plot_index[clicked_tab_name])


    def next_plot(self, tab_name: str) -> None:
        """
        Display the next plot for the given tab
        :param tab_name: Name of the tab to display the next plot for
        :return: None
        """
        self.plot_index[tab_name] = (self.plot_index[tab_name] + 1) % len(self.plots_container[tab_name])
        self.display_plot(tab_name, self.plot_index[tab_name])


    def previous_plot(self, tab_name: str) -> None:
        """
        Display the previous plot for the given tab
        :param tab_name: Name of the tab to display the previous plot for
        :return: None
        """
        self.plot_index[tab_name] = (self.plot_index[tab_name] - 1) % len(self.plots_container[tab_name])
        self.display_plot(tab_name, self.plot_index[tab_name])
