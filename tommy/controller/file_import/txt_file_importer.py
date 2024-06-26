import os
from datetime import datetime
from typing import Generator

from tommy.controller.file_import import file_importer_base
from tommy.controller.file_import.metadata import Metadata
from tommy.controller.file_import.raw_body import RawBody
from tommy.controller.file_import.raw_file import RawFile


class TxtFileImporter(file_importer_base.FileImporterBase):
    """
    Handles importing of txt files
    """

    def __init__(self) -> None:
        """
        Initializes a new instance of the class.
        """
        pass

    def compatible_file(self, path: str) -> bool:
        """
        A txt file is compatible with this parser if and only if
        it can be opened and read without errors.

        :param path: The string path to the txt file to be checked for
                     compatibility.

        :return: bool: True if the file is compatible, False otherwise.
        """

        if not path.endswith('.txt'):
            return False

        return True

    def load_file(self, path: str) -> Generator[RawFile, None, None]:
        """
        Loads a txt file and yields a File object.

        :param path: The string path to the txt file.
        :return: Generator[RawFile, None, None]: A generator yielding
        File objects.
        """
        with open(path, "r", encoding='utf-8-sig') as txtFile:
            text = txtFile.read()
            yield self.generate_file(text, path)

    @staticmethod
    def generate_file(text: str, path) -> RawFile:
        """
        Generates a File object from a txt file.

        :param text: A string representing the text of the txt file.
        :param path: The string path to the txt file.
        :return: A RawFile object generated from the txt file
        containing metadata and the raw text of the file.
        """

        alt_title = os.path.basename(path).replace('.txt', '')

        try:
            mod_time = os.path.getmtime(path)
            file_date = datetime.fromtimestamp(mod_time)
        except Exception:
            # If unable to get the modification time, don't set a date
            file_date = None

        return RawFile(
            metadata=Metadata(author=None,
                              title=alt_title,
                              date=file_date,
                              url=None,
                              path=path,
                              format="txt",
                              length=len(text.split(" ")),
                              name=alt_title,
                              size=os.stat(path).st_size),
            body=RawBody(body=text))


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University
(Department of Information and Computing Sciences)
"""
