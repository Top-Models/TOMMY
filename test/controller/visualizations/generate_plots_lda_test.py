import pytest
from gensim import models, corpora
import pickle

from tommy.controller.visualizations.visualization_input_datatypes import (
    MetadataCorpus, ProcessedCorpus)

from tommy.model.topic_model import TopicModel
from tommy.controller.topic_modelling_runners.lda_runner import LdaRunner
from tommy.controller.file_import.metadata import Metadata

from tommy.controller.visualizations.correlation_matrix_creator import (
    CorrelationMatrixCreator)
from tommy.controller.visualizations.document_word_count_creator import (
    DocumentWordCountCreator)
from tommy.controller.visualizations.top_words_bar_plot_creator import (
    TopWordsBarPlotCreator)
from tommy.controller.visualizations.word_cloud_creator import (
    WordCloudCreator)
from tommy.controller.visualizations.word_topic_network_creator import \
    WordTopicNetworkCreator
from tommy.controller.visualizations.document_topic_network_summary_creator import \
    DocumentTopicNetworkSummaryCreator


@pytest.fixture
def lda_model():
    # Load lda model which has 4 topics
    model = models.LdaModel.load('../../test_data/test_lda_model/lda_model')
    return model

@pytest.fixture
def lda_model_dictionary():
    dictionary = (corpora.Dictionary.load
                  ('../../test_data/test_lda_model/lda_model.id2word'))
    return dictionary


@pytest.fixture
def lda_runner(lda_model, lda_model_dictionary, mocker):
    topic_model = TopicModel()
    mocker.patch.object(LdaRunner, 'train_model')
    mocker.patch.object(LdaRunner, 'get_n_topics', return_value=4)
    lda_runner = LdaRunner(topic_model, [], 0, 0)
    lda_runner._model = lda_model
    lda_runner._dictionary = lda_model_dictionary
    return lda_runner


@pytest.fixture
def metadata():
    docs = [267, 1081, 75, 331, 1052, 544, 296, 460, 573, 335, 288, 209, 553,
            347, 283, 529, 1868, 384, 247, 391, 458, 910, 914, 584, 974, 611,
            145, 2118, 593, 474, 203, 585, 147, 1622, 319, 543, 330, 207, 299,
            278, 729, 580, 74, 774, 651, 647, 706, 8464, 305, 1559, 155, 180,
            172, 223, 705, 822, 64, 207, 497, 287, 96, 63, 472, 235, 223, 993,
            64, 176, 238, 16074, 509, 210, 154, 807, 311, 264, 307, 174, 257,
            401, 262, 550, 138, 223, 672, 1285, 424, 124, 145, 193, 705, 431,
            653, 1010, 592, 148, 573, 339, 242, 411, 13358, 289, 889, 173, 505,
            298, 642, 263, 1645, 274, 213, 185, 1137, 254, 87, 221, 5656, 668,
            376, 619, 383, 408, 380, 502, 372, 2198, 2406, 158, 127, 81, 604,
            534, 200, 1095, 167, 517, 1242, 112, 749, 162, 79, 1108, 73, 648,
            185, 258, 1987, 520, 54, 251, 333, 453, 1005, 612, 1284, 3770,
            1112, 1159, 521, 519, 147, 237, 523, 222, 279, 541, 317, 57, 140,
            279, 572, 573, 618, 179, 380, 478, 209, 424, 708, 734, 413, 121,
            401, 254, 196, 164, 194, 2359, 530, 27, 145, 1480, 746, 750, 585,
            305, 264, 601, 581, 69, 1186, 463, 79, 157, 400, 1893, 178, 8474,
            392, 165, 68, 69, 1150, 241, 8335, 282, 449, 240, 427, 9548, 292,
            116, 521, 268, 393, 622, 183, 1007, 168, 209, 642, 383, 163, 637,
            267, 575, 562, 728, 189, 836, 505, 548, 112, 11714, 648, 861, 9327,
            431, 142, 619, 2031, 166, 83, 563, 312, 359, 287, 558, 423, 561,
            497, 429, 2116, 1543, 297, 358, 115, 560, 616, 335, 1250, 237, 430,
            1894, 286, 997, 835, 142, 80, 139, 412, 169, 521, 510, 549, 647,
            382, 351, 180, 60, 277, 586, 67, 155, 279, 1512, 332, 85, 87, 662,
            588, 55, 993, 595, 1597, 76, 942, 481, 775, 1827, 302, 358, 12749,
            40, 1244, 707, 566, 168, 556, 182, 337, 569, 640, 1939, 1032, 9073,
            101, 295, 475, 229, 543, 555, 252, 8552, 1061, 618, 561, 337, 65,
            148, 416, 1877, 919, 544, 248, 561, 208, 1614, 237, 438, 257, 276,
            1556, 582, 503, 902, 690, 2849, 551, 1239, 672, 750, 533, 326, 686,
            182, 610, 214, 50, 46, 364, 390, 367, 513, 369, 982, 100, 1027,
            992, 480, 81, 8445, 125, 212, 282, 175, 174, 320, 1523, 304, 150,
            329, 283, 1096, 319, 329, 679, 726, 609, 482, 3543, 900, 261, 8187,
            544, 660, 861, 212, 1375, 166, 1111, 1057, 1557, 512, 71, 574, 449,
            213]

    return [Metadata(name='', size=0, length=length, format='')
            for length in docs]

@pytest.fixture
def processed_files():
    with open('../../test_data/test_processed_files/processed_files.pkl', 'rb') as f:
        processed_files = pickle.load(f)
        return processed_files

def test_generate_correlation_matrix(lda_runner):
    correlation_matrix = CorrelationMatrixCreator()
    figure = correlation_matrix._create_figure(lda_runner)
    assert figure


def test_generate_document_word_count(lda_runner, metadata):
    document_word_count = DocumentWordCountCreator()
    figure = document_word_count._create_figure(lda_runner, metadata)
    assert figure


@pytest.mark.parametrize("topic_id", [0, 1, 2, 3])
def test_generate_top_words_bar_plot(lda_runner, topic_id):
    top_words_bar_plot = TopWordsBarPlotCreator()
    figure = top_words_bar_plot._create_figure(lda_runner, topic_id)
    assert figure


@pytest.mark.parametrize("topic_id", [0, 1, 2, 3])
def test_generate_word_cloud(lda_runner, topic_id):
    word_cloud_creator = WordCloudCreator()
    figure = word_cloud_creator._create_figure(lda_runner, topic_id)
    assert figure


def test_generate_word_topic_network(lda_runner):
    word_topic_network = WordTopicNetworkCreator()
    figure = word_topic_network._create_figure(lda_runner)
    assert figure


def test_generate_document_topic_network_summary(lda_runner, processed_files):
    document_topic_network_summary = DocumentTopicNetworkSummaryCreator()
    figure = document_topic_network_summary._create_figure(lda_runner,
                                                           processed_files)
    figure.show()
    assert figure

