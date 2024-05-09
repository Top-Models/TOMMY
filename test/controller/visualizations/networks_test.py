import pytest
from gensim import models, corpora
import networkx as nx
import pickle
import os

from tommy.model.topic_model import TopicModel
from tommy.controller.topic_modelling_runners.lda_runner import LdaRunner

from tommy.controller.visualizations.word_topic_nx_exporter import (
    WordTopicNxExporter)
from tommy.controller.visualizations.document_topic_nx_exporter import (
    DocumentTopicNxExporter)


# Test data directory
TEST_DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                             '..',
                                             '..',
                                             '..',
                                             'test',
                                             'test_data'))


@pytest.fixture
def lda_model():
    # Load saved lda model which has 4 topics
    path = os.path.join(TEST_DATA_DIR, 'test_lda_model', 'lda_model')
    model = models.LdaModel.load(path)
    return model


@pytest.fixture
def lda_model_dictionary():
    # Load id2word file of saved lda model
    path = os.path.join(TEST_DATA_DIR, 'test_lda_model', 'lda_model.id2word')
    dictionary = (corpora.Dictionary.load(path))
    return dictionary


@pytest.fixture
def processed_files():
    # Load saved processed files
    path = os.path.join(TEST_DATA_DIR,
                        'test_processed_files',
                        'processed_files.pkl')
    with open(path, 'rb') as file:
        processed_files = pickle.load(file)
        return processed_files


@pytest.fixture
def lda_runner(lda_model, lda_model_dictionary, mocker):
    topic_model = TopicModel()

    # Mock LdaRunner functions
    mocker.patch.object(LdaRunner, 'train_model')
    mocker.patch.object(LdaRunner, 'get_n_topics', return_value=4)

    # Construct a mocked instance of LdaRunner
    lda_runner = LdaRunner(topic_model, [], 0, 0)
    lda_runner._model = lda_model
    lda_runner._dictionary = lda_model_dictionary
    return lda_runner


@pytest.mark.parametrize("node_amount", [1, 2, 3, 4, 5, 8, 15, 21, 50])
def test_word_topic_graph_size(lda_runner, node_amount):
    exporter = WordTopicNxExporter()
    graph = exporter.construct_word_topic_network(lda_runner, node_amount)
    topic_amount = lda_runner.get_n_topics()

    # Assert - The number of nodes should not exceed the amount of topic nodes
    # plus the amount of word nodes (topic_amount * node_amount)
    assert graph.number_of_nodes() <= topic_amount * node_amount + topic_amount

    # Assert
    assert graph.number_of_edges() == topic_amount * node_amount


@pytest.mark.parametrize("probability", [0.0, 0.01, 0.05, 0.1, 0.24, 80])
def test_document_topic_graph_size(lda_runner, processed_files, probability):
    exporter = DocumentTopicNxExporter()
    graph = exporter.construct_doc_topic_network(lda_runner,
                                                 processed_files,
                                                 0.05)
    topic_amount = lda_runner.get_n_topics()

    # Assert - The number of nodes should not change when probability changes
    assert graph.number_of_nodes() == topic_amount + len(processed_files)

    # Assert - The number of edges should not exceed topic amount times the
    # amount of files
    assert graph.number_of_edges() <= topic_amount * len(processed_files)


