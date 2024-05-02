from pypdf import PdfReader
import os.path
from os import stat
from typing import Generator

from tommy.controller.file_import import file_importer_base
from tommy.controller.file_import.metadata import Metadata
from tommy.controller.file_import.raw_body import RawBody
from tommy.controller.file_import.raw_file import RawFile


class PdfFileImporter(file_importer_base.FileImporterBase):
    """
    Handles importing of PDF files
    """

    def __init__(self) -> None:
        """
        Initializes a new instance of the class.
        """
        pass

    def compatible_file(self, path: str) -> bool:
        """
        A PDF file is compatible with this parser if and only if
        the file extension is .pdf

        :param path: The string path to the PDF file to be checked for
                     compatibility.
        :return: bool: True if the file is compatible, False otherwise.
        """
        return path.endswith('.pdf')

    def load_file(self, path: str) -> Generator[RawFile, None, None]:
        """
        Loads a PDF file and yields File objects.

        :param path: The string path to the PDF file.
        :return: File: A File object generated from each page of the PDF.
        """
        try:
            with open(path, 'rb') as file:
                pdf = PdfReader(file)
                metadata = pdf.metadata

                # Bundle all pages together into one document
                text = ''
                for page in pdf.pages:
                    text += page.extract_text()
                yield self.generate_file(text, path, metadata)
        except Exception as e:
            print(f"Failed to load file {path} due to error: {e}")

    def generate_file(self, file: str, path, metadata) -> RawFile:
        """
        Generates a File object from a PDF page.

        :param file: A string representing a page of PDF data.
        :param path: The string path to the PDF file.
        :return: A RawFile object generated from the PDF page
        containing metadata and the raw text of the file.
        """

        alt_title = os.path.basename(path).replace('.pdf', '')

        return RawFile(
                metadata=Metadata(author=metadata.get('/Author', None),
                                  title=alt_title,
                                  date=metadata.get('/ModDate', None),
                                  path=os.path.relpath(path),
                                  format="pdf",
                                  length=len(file.split(" ")),
                                  name=alt_title,
                                  size=stat(path).st_size),
                body=RawBody(body=file))

