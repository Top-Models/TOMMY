import os
from typing import Generator

from tommy.controller.file_import import csv_file_importer
from tommy.controller.file_import import docx_file_importer
from tommy.controller.file_import import file_importer_base
from tommy.controller.file_import import pdf_file_importer
from tommy.controller.file_import import txt_file_importer
from tommy.controller.file_import.raw_file import RawFile


class GenericFileImporter:
    """
    The class GenericFileImporter is responsible for importing files using
     FileImporterBase objects
    """

    def __init__(self):
        """
        Initialization of a new GenericFileImporter object.
        """
        self.importers: (
            list)[file_importer_base.FileImporterBase] = [
            docx_file_importer.DocxFileImporter(),
            pdf_file_importer.PdfFileImporter(),
            csv_file_importer.CsvFileImporter(),
            txt_file_importer.TxtFileImporter(),
        ]

    def import_file(self, path: str) -> Generator[RawFile, None, None]:
        """
        Imports a file from the specified path using compatible importers.

        :param path: The string path of the file to import.
        :return Generator[File, None, None]: A generator yielding File objects.
        """
        path = os.path.normpath(path)

        for importer in self.importers:
            if importer.compatible_file(path):
                return importer.load_file(path)
        raise NotImplementedError("File does not have a compatible file "
                                  "importer implementation. Path:", path)


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University
(Department of Information and Computing Sciences)
"""
