from PySide6.QtWidgets import QWidget, QTabWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import numpy as np
from gensim import corpora, models
import gensim.downloader as api
from wordcloud import WordCloud

# Assuming you have this import statement
from interactive_topic_modeling.display.topic_display.fetched_topics_display import FetchedTopicsDisplay


class GraphDisplay(QTabWidget):
    num_topics = 5

    def __init__(self):
        super().__init__()

        # Initialize widget properties
        self.setStyleSheet("""
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
        lda_model = self.perform_lda_on_text(self.sample_text)

        # Event handling
        self.tabBarClicked.connect(self.on_tab_clicked)

    # Preprocess the text and tokenize it
    def preprocess_text(self, text) -> list:
        tokens = text.lower().split()
        return tokens

    def get_wordcloud_canvasses(self, figures):
        canvas_list = []
        for figure in figures:
            canvas_list.append(FigureCanvas(figure))
        return canvas_list

    def construct_wordcloud(self, lda_model):
        wordclouds = []
        for topic_id, topic in enumerate(lda_model.print_topics(num_topics=self.num_topics, num_words=20)):

            topic_words = " ".join([word.split("*")[1].strip() for word in topic[1].split(" + ")])
            wordcloud = WordCloud(width=800, height=800, random_state=15, max_font_size=110).generate(topic_words)

            # Create a Matplotlib figure and canvas
            fig, ax = plt.subplots()
            ax.imshow(wordcloud, interpolation="bilinear")
            ax.axis("off")
            ax.set_title("Topic {}".format(topic_id))

            wordclouds.append(fig)
        return wordclouds


    def on_tab_clicked(self, index) -> None:
        """
        Event handler for when a tab is clicked
        :param index: Index of the clicked tab
        :return: None
        """

        clicked_tab_name = self.tabText(index)
        self.fetched_topics_display.display_topics(clicked_tab_name)

    def perform_lda_on_text(self, text):
        # Preprocess the text
        preprocessed_text = self.preprocess_text(text)

        # Create a dictionary from the preprocessed text
        dictionary = corpora.Dictionary([preprocessed_text])

        # Create a bag-of-words representation of the corpus
        corpus = [dictionary.doc2bow(preprocessed_text)]

        # Train the LDA model
        lda_model = models.LdaModel(corpus, num_topics=self.num_topics, id2word=dictionary, passes=100)

        return lda_model
