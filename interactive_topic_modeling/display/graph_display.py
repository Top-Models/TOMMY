from PySide6.QtWidgets import QWidget, QTabWidget, QVBoxLayout, QPushButton
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from gensim import corpora, models

# Assuming you have this import statement
from interactive_topic_modeling.display.topic_display.fetched_topics_display import FetchedTopicsDisplay


def preprocess_text(text) -> list:
    tokens = text.lower().split()
    return tokens


def perform_lda_on_text(text):
    # Preprocess the text
    preprocessed_text = preprocess_text(text)

    # Create a dictionary from the preprocessed text
    dictionary = corpora.Dictionary([preprocessed_text])

    # Create a bag-of-words representation of the corpus
    corpus = [dictionary.doc2bow(preprocessed_text)]

    # Train the LDA model
    lda_model = models.LdaModel(corpus, num_topics=5, id2word=dictionary, passes=10)

    return lda_model


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
        lda_model = perform_lda_on_text(self.sample_text)

        # Get active tab name
        active_tab_name = self.tabText(self.currentIndex())

        # Add LDA plots to active tab
        self.add_lda_plots(active_tab_name, lda_model)

        # Event handling
        self.tabBarClicked.connect(self.on_tab_clicked)

        self.display_plot(active_tab_name, 0)

    def add_lda_plots(self, tab_name: str, lda_model) -> None:
        """
        Add a word cloud plot for the given LDA model
        :param tab_name: Name of the tab to add the plot to
        :param lda_model: The LDA model to add a plot for
        :return: None
        """
        plots = []
        self.plot_index[tab_name] = 0
        self.plots_container[tab_name] = []

        plots.extend(self.construct_wordclouds(tab_name, lda_model))

        for plot in plots:
            self.plots_container[tab_name].append(plot)

    def construct_wordclouds(self, tab_name: str, lda_model):
        canvases = []
        for topic_id, topic in enumerate(lda_model.print_topics(num_topics=5, num_words=20)):
            topic_words = " ".join([word.split("*")[1].strip() for word in topic[1].split(" + ")])
            wordcloud = WordCloud(width=800, height=800, random_state=15, max_font_size=110).generate(topic_words)

            # Add topics to topic display
            self.fetched_topics_display.add_topic(
                tab_name,
                f"Topic {topic_id}",
                topic_words.split())

            # Create a Matplotlib figure and canvas
            fig, ax = plt.subplots()
            ax.imshow(wordcloud, interpolation="bilinear")
            ax.axis("off")
            ax.set_title("Topic: {}".format(topic_id))

            canvases.append(FigureCanvas(fig))
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
