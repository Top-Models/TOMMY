from dataclasses import dataclass

from tommy.support.types import Processed_body


@dataclass
class ProcessedBody:
    """
    The ProcessedBody class contains a bag of words representation of a
    document after pre-processing.
    """
    body: Processed_body


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University
(Department of Information and Computing Sciences)
"""
