import os.path
from os import stat
from typing import Generator

from pypdf import PdfReader, DocumentInformation

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
        the file extension is .pdf and the file is not corrupted.

        :param path: The string path to the PDF file to be checked for
                     compatibility.
        :return: bool: True if the file is compatible, False otherwise.
        """
        if not path.endswith('.pdf'):
            return False

        with open(path, 'rb') as file:
            PdfReader(file)
        return True

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
        except Exception as e:
            raise Exception(f"kon niet correct gelezen worden: {e}")

        yield self.generate_file(text, path, metadata)

    @staticmethod
    def generate_file(file: str, path: str, metadata: DocumentInformation) -> (
            RawFile):
        """
        Generates a File object from a PDF page.

        :param file: A string representing a page of PDF data.
        :param path: The string path to the PDF file.
        :param metadata: The metadata of the PDF file.
        :return: A RawFile object generated from the PDF page
        containing metadata and the raw text of the file.
        """

        alt_title = os.path.basename(path).replace('.pdf', '')

        try:
            date = metadata.creation_date
        except Exception:
            # If unable to get the modification time, don't set a date
            date = None

        return RawFile(
            metadata=Metadata(author=metadata.get('/Author', None),
                              title=metadata.get('/Title', alt_title),
                              date=date,
                              path=os.path.relpath(path),
                              format="pdf",
                              length=len(file.split(" ")),
                              name=alt_title,
                              size=stat(path).st_size),
            body=RawBody(body=file))


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University
(Department of Information and Computing Sciences)
"""
