from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton

from tommy.controller.corpus_controller import CorpusController


class ReadInFilesButton(QWidget):
    """
    The ReadInFilesButton class that defines the button to
    read in files.
    """

    def __init__(self) -> None:
        """Initialize the button."""
        super().__init__()

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
        """Read the files with the file reader."""
        # this assumes that the ProjectSettingsController already has
        # the input folder selected
        fileGenerator = CorpusController.get_raw_bodies()
        # Apply all other functions like preprocessing here



"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University 
(Department of Information and Computing Sciences)
"""
