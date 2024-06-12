from dataclasses import dataclass

import networkx as nx
from matplotlib.figure import Figure


@dataclass
class NxExport:
    vis_name: str
    graph: nx.graph


@dataclass
class MatplotLibExport:
    vis_name: str
    topic_num: int | None
    figure: Figure


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University
(Department of Information and Computing Sciences)
"""
