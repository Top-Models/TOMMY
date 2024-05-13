from dataclasses import dataclass
from enum import Enum


class VisGroup(Enum):
    """An enumeration of the groups of visualizations. The groups are TOPIC
    for plots about one single topic, MODEL for plots about the entire topic
    modelling run, and CORPUS for plots about the input corpus."""
    TOPIC = 1
    MODEL = 2
    CORPUS = 3


@dataclass
class PossibleVisualization:
    index: int
    name: str
    short_tab_name: str
    type: VisGroup
    needs_topic: bool


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University
(Department of Information and Computing Sciences)
"""
