from dataclasses import dataclass
from datetime import date


@dataclass
class File:
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
