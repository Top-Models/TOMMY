from dataclasses import dataclass
from datetime import date


@dataclass
class File:
    name: str
    size: int
    content: str
    body: str
    length = len(content.split())
    format: str = name.split(".")[-1]
    author: str = None
    title: str = None
    date: date = None
    url: str = None
    path: str = None
