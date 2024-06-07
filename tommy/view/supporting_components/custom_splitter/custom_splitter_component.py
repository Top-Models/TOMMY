from PySide6.QtWidgets import QSplitter

from tommy.view.supporting_components.custom_splitter.custom_splitter_handle \
    import (CustomSplitterHandle)


class CustomSplitter(QSplitter):
    """Custom splitter to use the custom handle."""

    def __init__(self, orientation, parent=None):
        super().__init__(orientation, parent)

    def createHandle(self):
        return CustomSplitterHandle(self.orientation(), self)


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University
(Department of Information and Computing Sciences)
"""
