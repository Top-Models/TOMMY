from datetime import datetime

import pandas as pd
import pytest

from tommy.controller.visualizations.documents_over_time_creator import (
    DocumentsOverTimeCreator)
from tommy.controller.visualizations.documents_over_time_per_topic_creator \
    import DocumentsOverTimePerTopicCreator


@pytest.fixture
def dataframe():
    data = {"date": [datetime(2024, 4, 20),
                     datetime(2026, 1, 1),
                     datetime(2026, 1, 2)],
            "probability": [0.69, 0.420, 0.666]}
    df = pd.DataFrame(data)
    return df


def test_get_valid_offsets(dataframe):
    offsets = DocumentsOverTimeCreator._get_valid_offsets()
    for offset in offsets:
        grouped_df = dataframe.groupby([pd.Grouper(key='date',
                                                       freq=offset)],
                                       as_index=False)["probability"].sum()
        assert not grouped_df.empty


def test_get_valid_offsets_per_topic(dataframe):
    offsets = DocumentsOverTimePerTopicCreator._get_valid_offsets()
    for offset in offsets:
        grouped_df = dataframe.groupby([pd.Grouper(key='date',
                                                   freq=offset)],
                                       as_index=False)["probability"].sum()
        assert not grouped_df.empty


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University
(Department of Information and Computing Sciences)
"""
