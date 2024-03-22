from dataclasses import dataclass

from tommy.controller.file_import.metadata import Metadata
from tommy.controller.file_import.raw_body import RawBody


@dataclass
class RawFile:
    """
    Represents the raw text and metadata of a file
    """
    body: RawBody
    metadata: Metadata


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University
(Department of Information and Computing Sciences)
"""
