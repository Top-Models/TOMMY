import os
import tempfile
import networkx as nx
import matplotlib.pyplot as plt
from tommy.controller.export_controller import ExportController
from tommy.controller.graph_controller import GraphController

# Mocked GraphController
class MockGraphController(GraphController):
    def get_all_nx_exports(self):
        G1 = nx.Graph()
        G2 = nx.DiGraph()
        return [G1, G2]

    def get_all_visualizations(self):
        fig1 = plt.figure()
        fig2 = plt.figure()
        return [fig1, fig2]

    def get_number_of_topics(self):
        return 3

    def get_topic_with_scores(self, topic_index, num_words):
        return TopicWithScores(top_words=['word1', 'word2', 'word3'],
                               word_scores=[0.1, 0.2, 0.3])

class TopicWithScores:
    def __init__(self, top_words, word_scores):
        self.top_words = top_words
        self.word_scores = word_scores

def test_export_networks():
    # Setup
    export_controller = ExportController()
    export_controller.set_controller_refs(MockGraphController())
    with tempfile.TemporaryDirectory() as tmpdirname:
        # Exercise
        export_controller.export_networks(tmpdirname)
        # Verify
        assert os.path.isfile(os.path.join(tmpdirname, '0.gexf'))
        assert os.path.isfile(os.path.join(tmpdirname, '1.gexf'))

def test_export_graphs():
    # Setup
    export_controller = ExportController()
    export_controller.set_controller_refs(MockGraphController())
    with tempfile.TemporaryDirectory() as tmpdirname:
        # Exercise
        export_controller.export_graphs(tmpdirname)
        # Verify
        assert os.path.isfile(os.path.join(tmpdirname, '0.png'))
        assert os.path.isfile(os.path.join(tmpdirname, '1.png'))

def test_export_topic_words_csv():
    # Setup
    export_controller = ExportController()
    export_controller.set_controller_refs(MockGraphController())
    with tempfile.TemporaryDirectory() as tmpdirname:
        csv_path = os.path.join(tmpdirname, 'test_export.csv')
        # Exercise
        export_controller.export_topic_words_csv(csv_path)
        # Verify
        assert os.path.isfile(csv_path)
        with open(csv_path, 'r') as f:
            lines = f.readlines()
            assert len(lines) == 4  # Header + 3 topic rows
            assert lines[0].strip() == 'Topic,Word,Score'
            assert lines[1].strip() == 'Topic 1,word1,0.1'
            assert lines[2].strip() == 'Topic 1,word2,0.2'
            assert lines[3].strip() == 'Topic 1,word3,0.3'
