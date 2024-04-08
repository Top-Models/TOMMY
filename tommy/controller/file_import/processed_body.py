from dataclasses import dataclass
from typing import Any


@dataclass
class ProcessedBody:
    """
    The ProcessedBody class contains a bag of words representation of a
    document after pre-processing.
    """
    body: Any
