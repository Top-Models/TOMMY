from collections.abc import Iterable
from enum import Enum

from tommy.controller.file_import.metadata import Metadata
from tommy.controller.file_import.processed_file import ProcessedFile


class VisInputData(Enum):
    """An enumeration of the different kinds of input data that a visualization
    can need."""
    TOPIC_ID = 1
    METADATA_CORPUS = 2
    PROCESSED_CORPUS = 3


# the data types of the input data for the visualizations. These correspond
#   one-to-one to the entries in the VisInputData enumerator above.
type TopicID = int
type MetadataCorpus = list[Metadata]
type ProcessedCorpus = Iterable[ProcessedFile]

"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University
(Department of Information and Computing Sciences)
"""
