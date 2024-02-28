from dataclasses import dataclass
from datetime import datetime


@dataclass
class File:
    body: str
    author: str = None
    title: str = None
    date: datetime = None
    url: str = None
    path: str = None
