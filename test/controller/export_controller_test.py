import csv
import os
from unittest.mock import MagicMock

import pytest

from tommy.controller.export_controller import ExportController
from tommy.controller.graph_controller import GraphController
from tommy.controller.topic_modelling_controller import \
    TopicModellingController


# Mock metadata
class MockMetadata:
    def __init__(self, name, format, length, author, title, date, path):
        self.name = name
        self.format = format
        self.length = length
        self.author = author
        self.title = title
        self.date = date
        self.path = path

# Mock data
DOCUMENT_TOPICS = [
    (MockMetadata('doc1', 'txt', 123, 'author1', 'title1', '2023-01-01', '/path1'), [0.1, 0.9]),
    (MockMetadata('doc2', 'pdf', 456, 'author2', 'title2', '2023-01-02', '/path2'), [0.3, 0.7]),
    (MockMetadata('doc3', 'docx', 789, 'author3', 'title3', '2023-01-03', '/path3'), [0.4, 0.6]),
]


@pytest.fixture
def mock_graph_controller():
    mock_controller = MagicMock(spec=GraphController)
    mock_controller.get_number_of_topics.return_value = 2
    mock_controller.get_topic_with_scores.side_effect = [
        MagicMock(top_words=['word1', 'word2'], word_scores=[0.9, 0.8]),
        MagicMock(top_words=['word3', 'word4'], word_scores=[0.7, 0.6]),
    ]
    return mock_controller


@pytest.fixture
def mock_topic_modelling_controller():
    mock_controller = MagicMock(spec=TopicModellingController)
    return mock_controller


@pytest.fixture
def export_controller(mock_graph_controller, mock_topic_modelling_controller):
    controller = ExportController()
    controller.set_controller_refs(mock_graph_controller,
                                   mock_topic_modelling_controller)
    controller.document_topics = DOCUMENT_TOPICS
    return controller


def test_export_topic_words_csv(export_controller, tmp_path):
    temp_csv_path = tmp_path / "topics.csv"
    export_controller.export_topic_words_csv(temp_csv_path)

    with open(temp_csv_path, mode='r') as file:
        csv_reader = csv.reader(file)
        rows = list(csv_reader)

    assert rows[0] == ['Topic', 'Word', 'Score']
    assert rows[1] == ['Topic 1', 'word1', '0.9']
    assert rows[2] == ['Topic 1', 'word2', '0.8']
    assert rows[3] == ['Topic 2', 'word3', '0.7']
    assert rows[4] == ['Topic 2', 'word4', '0.6']

    os.remove(temp_csv_path)


def test_export_document_topics_csv(export_controller, tmp_path):
    temp_csv_path = tmp_path / "document_topics.csv"
    export_controller.export_document_topics_csv(temp_csv_path)

    with open(temp_csv_path, mode='r') as file:
        csv_reader = csv.reader(file)
        rows = list(csv_reader)

    # Verify header row
    assert rows[0] == ['Filename', 'Length', 'Author', 'Title', 'Date', 'Path', 'Topic 1 Probability', 'Topic 2 Probability']

    # Verify document topic rows
    assert rows[1] == ['doc1.txt', '123', 'author1', 'title1', '2023-01-01', '/path1', '0.1', '0.9']
    assert rows[2] == ['doc2.pdf', '456', 'author2', 'title2', '2023-01-02', '/path2', '0.3', '0.7']
    assert rows[3] == ['doc3.docx', '789', 'author3', 'title3', '2023-01-03', '/path3', '0.4', '0.6']

    os.remove(temp_csv_path)


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University
(Department of Information and Computing Sciences)
"""