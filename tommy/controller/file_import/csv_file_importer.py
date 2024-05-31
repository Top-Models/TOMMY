import csv
import os.path
from os import stat
from typing import Generator
from datetime import date

from tommy.controller.file_import import file_importer_base
from tommy.controller.file_import.metadata import Metadata
from tommy.controller.file_import.raw_body import RawBody
from tommy.controller.file_import.raw_file import RawFile


class CsvFileImporter(file_importer_base.FileImporterBase):
    """
    Handles importing of csv files
    """
    mandatory_fields: list[str] = ['body']

    def __init__(self) -> None:
        """
        Initializes a new instance of the class.
        """
        pass

    def compatible_file(self, path: str) -> bool:
        """
        A CSV file is compatible with this parser if and only if
        the first row of the CSV file contains all mandatory headers

        :param path: The string path to the CSV file to be checked for
                     compatibility.
        :return: bool: True if the file is compatible, False otherwise.
        """
        if not path.endswith('.csv'):
            return False

        headers = []
        with open(path, 'r', newline="", encoding='utf-8-sig') as csvfile:
            csv_reader = csv.DictReader(csvfile, delimiter=',')
            headers = csv_reader.fieldnames
            # To check whether each mandatory header exists and is unique,
            # we keep an array of occurrences of all mandatory headers
            mandatory_fields_counts = [0] * len(self.mandatory_fields)
            for header in csv_reader.fieldnames:
                if header.lower() in self.mandatory_fields:
                    mandatory_fields_counts[self.mandatory_fields.index(
                        header.lower())] += 1

            if mandatory_fields_counts == [1] * len(self.mandatory_fields):
                return True

        raise ValueError("CSV bestand heeft niet alle verplichte headers, "
                         f"of te veel headers. Headers: {headers}")

    def load_file(self, path: str) -> Generator[RawFile, None, None]:
        """
        Loads a CSV file and yields File objects.

        :param path: The string path to the CSV file.
        :return: File: A File object generated from each row of the CSV.
        """
        with open(path, 'r', newline="", encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile)
            reader.fieldnames = [str(header).lower() for header in
                                 reader.fieldnames]
            row: dict

            row_index = 1  # Only used for debugging
            for row in reader:
                # Remove empty fields
                for key, value in row.items():
                    if value == "" or value.isspace():
                        del row[key]

                yield self.generate_file(row, path, row_index)
                row_index += 1

    def generate_file(self, file: dict, path, row_index) -> RawFile:
        """
        Generates a File object from a CSV row.

        :param file: A dictionary representing a row of CSV data.
        :param path: The string path to the CSV file.
        :return: A RawFile object generated from the CSV row
        containing metadata and the raw text of the file.
        """
        for key in self.mandatory_fields:
            if key not in file or file[key] is None:
                raise KeyError(f"er is een probleem opgetreden op rij "
                               f"{row_index}", key)

        file_date: str = file.get("date")
        if file_date is not None and not file_date.isspace():
            file_date: date = self.parse_date(file_date)
        return RawFile(
            metadata=Metadata(author=file.get("author"),
                              title=file.get("title"), date=file_date,
                              url=file.get("url"), path=os.path.relpath(path),
                              format="csv",
                              length=len(file.get("body").split(" ")),
                              name=os.path.relpath(path).split(".")[0],
                              size=stat(path).st_size),
            body=RawBody(body=file.get("body").strip()))


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University
(Department of Information and Computing Sciences)
"""
