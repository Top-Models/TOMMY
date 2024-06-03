from tommy.controller.file_import.metadata import Metadata

# This is a list of document metadata coupled with its list of probabilities
# of belonging to each topic, indices of list[float] are topic indices
Document_topics = list[tuple[Metadata, list[float]]]

# This is a list of tokens resulted from preprocessing
Processed_body = list[str]

"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University
(Department of Information and Computing Sciences)
"""
