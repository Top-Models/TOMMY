from dataclasses import dataclass

from gensim.corpora import Dictionary
from gensim.models import LdaModel


@dataclass
class TopicModel:
    """dataclass that holds the data and objects necessary to run a topic
    modelling algorithm"""
    model: LdaModel = None
    dictionary: Dictionary = None


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University 
(Department of Information and Computing Sciences)
"""
