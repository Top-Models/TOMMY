from typing import List, Any


class ProcessedCorpus:
    documentBows: List[Any] = None

    def __init__(self):
        pass

    def __iter__(self):
        return iter(self.documentBows)


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University 
(Department of Information and Computing Sciences)
"""
