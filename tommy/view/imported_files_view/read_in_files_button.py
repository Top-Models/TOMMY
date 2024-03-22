from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton

from tommy.controller.corpus_controller import CorpusController


class ReadInFilesButton(QWidget):
    """
    The ReadInFilesButton class that defines the button to
    read in files.
    """

    def __init__(self, corpus_controller: CorpusController) -> None:
        """Initialize the button."""
        super().__init__()

        self._corpus_controller = corpus_controller

        # Initialize layout
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Initialize button
        btn = QPushButton("Read in files", self)
        btn.setToolTip("Start reading in files from the selected folder")
        btn.resize(btn.sizeHint())
        btn.move(150, 0)
        btn.clicked.connect(self.read_files)

    def read_files(self) -> None:
        """
        Read the files with the file reader assuming that the
        ProjectSettingsController already has the input folder selected
        """
        fileGenerator = self._corpus_controller.get_raw_bodies()
        # Apply all other functions like preprocessing here
        # todo: connect this button to actual functionality,
        # it does not do anything right now.


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University 
(Department of Information and Computing Sciences)
"""
