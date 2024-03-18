from dataclasses import dataclass
from datetime import date


@dataclass
class File:
    """
    Represents a file object with various attributes.
    """
    name: str
    size: int
    body: str
    length: int
    format: str
    author: str = None
    title: str = None
    date: date = None
    url: str = None
    path: str = None


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University 
(Department of Information and Computing Sciences)
"""
