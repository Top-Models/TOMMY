from dataclasses import dataclass
from datetime import datetime


@dataclass
class Metadata:
    """
    Represents the metadata of a file with various attributes
    """
    name: str
    size: int
    length: int
    format: str
    author: str = None
    title: str = None
    date: datetime = None
    url: str = None
    path: str = None


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University
(Department of Information and Computing Sciences)
"""
