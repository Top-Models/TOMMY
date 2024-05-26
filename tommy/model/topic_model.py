from dataclasses import dataclass

from bertopic import BERTopic
from gensim.corpora import Dictionary
from gensim.models import LdaModel
from gensim.models.nmf import Nmf


@dataclass
class TopicModel:
    """dataclass that holds the data and objects necessary to run a topic
    modelling algorithm"""
    model: LdaModel | Nmf | BERTopic = None
    dictionary: Dictionary = None
    corpus: list[list[tuple[int, int]]] = None


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University
(Department of Information and Computing Sciences)
"""
