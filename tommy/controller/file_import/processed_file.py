from dataclasses import dataclass
from typing import Any

from tommy.controller.file_import.metadata import Metadata
from tommy.controller.file_import.processed_body import ProcessedBody


@dataclass
class ProcessedFile:
    """
    Contains information about a processed file. It contains both a
    reference to the metadata and a ProcessedBody object
    """
    metadata: Metadata
    body: ProcessedBody
    topic_correspondence: [float] = None


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University
(Department of Information and Computing Sciences)
"""
