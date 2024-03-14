import os
from typing import Generator

from interactive_topic_modeling.backend.file_import import (
    generic_file_importer)
from interactive_topic_modeling.backend.file_import.file import File


class FileReader:
    """
    FileReader is responsible for generating a sequence of files in a
    directory and its subdirectories.

    This class uses a GenericFileImporter object to import files.
    """
    def __init__(self):
        """
        The initialization of the object.
        """
        # The selected directory is part of the project settings,
        # so this is a dummy implementation and the selected directory
        # should be fetched from the project settings
        self.fileParsers = generic_file_importer.GenericFileImporter()

    def test_read_file(self) -> None:
        """
        Test method to print files fetched by the FileReader
        :return: None
        """
        print(list(self.read_files(os.path.pardir)))

    def read_files(self, path: str) -> Generator[File, None, None]:
        """
        Yields the contents of all compatible files in a given directory
        and all its subdirectories.

        :param path: The string of the path to the directory
        :return Generator[File, None, None]: A generator yielding File objects.
        """
        for root, dirs, files in os.walk(path):
            for file in files:
                yield from self.fileParsers.import_file(os.path.join(root,
                                                                     file))


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University 
(Department of Information and Computing Sciences)
"""
