import os
from typing import Generator
import mammoth

from tommy.controller.file_import import file_importer_base
from tommy.controller.file_import.metadata import Metadata
from tommy.controller.file_import.raw_body import RawBody
from tommy.controller.file_import.raw_file import RawFile


class DocxFileImporter(file_importer_base.FileImporterBase):
    """
    Handles importing of Word files
    """

    def __init__(self) -> None:
        """
        Initializes a new instance of the class.
        """
        pass

    def compatible_file(self, path: str) -> bool:
        """
        A Word file is compatible with this parser if and only if
        it can be opened and read without errors.

        :param path: The string path to the Word file to be checked for
                     compatibility.
        :return: bool: True if the file is compatible, False otherwise.
        """

        if not path.endswith('.docx'):
            return False

        try:
            with open(path, "rb") as docx_file:
                mammoth.extract_raw_text(docx_file)
            return True
        except Exception as e:
            print(f"Error reading file '{path}': {e}")
            return False

    def load_file(self, path: str) -> Generator[RawFile, None, None]:
        """
        Loads a Word file and yields a File object.

        :param path: The string path to the Word file.
        :return: Generator[RawFile, None, None]: A generator yielding File objects.
        """
        with open(path, "rb") as docx_file:
            result = mammoth.extract_raw_text(docx_file)
            text = result.value  # Extracted text
            yield self.generate_file(text, path)

    def generate_file(self, text: str, path) -> RawFile:
        """
        Generates a File object from a Word file.

        :param text: A string representing the text of the Word file.
        :param path: The string path to the Word file.
        :return: A RawFile object generated from the Word file
        containing metadata and the raw text of the file.
        """

        alt_title = os.path.basename(path).replace('.docx', '')

        return RawFile(
            metadata=Metadata(author=None,
                              title=alt_title,
                              date=None,
                              url=None,
                              path=path,
                              format="docx",
                              length=len(text.split(" ")),
                              name=alt_title,
                              size=os.stat(path).st_size),
            body=RawBody(body=text))
