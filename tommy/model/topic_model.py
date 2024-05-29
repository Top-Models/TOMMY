from dataclasses import dataclass

from gensim.corpora import Dictionary
from gensim.models import LdaModel
from gensim.models.nmf import Nmf

from tommy.support.types import Document_topics


@dataclass
class TopicModel:
    """dataclass that holds the data and objects necessary to run a topic
    modelling algorithm"""
    model: LdaModel | Nmf = None
    dictionary: Dictionary = None
    corpus: list[list[tuple[int, int]]] = None
    document_topics: Document_topics = None
    used_corpus_version_id: int = None


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University
(Department of Information and Computing Sciences)
"""
