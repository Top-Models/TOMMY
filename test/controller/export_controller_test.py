import pytest
from unittest.mock import MagicMock
import csv
import os

from tommy.controller.export_controller import ExportController
from tommy.controller.graph_controller import GraphController


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
def export_controller(mock_graph_controller):
    controller = ExportController()
    controller.set_controller_refs(mock_graph_controller)
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
