import pytest
import pandas as pd
from tommy.controller.visualizations.documents_over_time_creator import (
    DocumentsOverTimeCreator)
from tommy.controller.visualizations.documents_over_time_per_topic_creator \
    import DocumentsOverTimePerTopicCreator

@pytest.fixture
def dataframe():
    data = {"date": [],
            "probability": []}


def test_get_valid_offsets():
    offsets = DocumentsOverTimeCreator._get_valid_offsets()
    #prefixes = [offset._prefix for offset in pd.offsets.__all__]
    prefixes = [offset.to_offset() for offset in offsets]
    print(prefixes)
    assert False


def test_get_valid_offsets_per_topic():
    offsets = DocumentsOverTimePerTopicCreator._get_valid_offsets()
    print(offsets)
    assert True
