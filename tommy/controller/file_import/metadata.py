from dataclasses import dataclass
from datetime import date


@dataclass
class Metadata:
    """
    Represents the metadata of a file with various attributes
    """
    path: str
    name: str
    size: int
    length: int
    format: str
    author: str = None
    title: str = None
    date: date = None
    url: str = None


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University
(Department of Information and Computing Sciences)
"""
