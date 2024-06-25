import csv
import os.path
from datetime import datetime
from os import stat
from typing import Generator

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

        with open(path, 'r', newline="", encoding='utf-8-sig') as csvfile:
            csv_reader = csv.DictReader(csvfile, delimiter=',')

            # To check whether each mandatory header exists and is unique,
            # we keep an array of occurrences of all mandatory headers
            mandatory_fields_counts = [0] * len(self.mandatory_fields)
            for header in csv_reader.fieldnames:
                if header.lower() in self.mandatory_fields:
                    mandatory_fields_counts[self.mandatory_fields.index(
                        header.lower())] += 1

            if mandatory_fields_counts == [1] * len(self.mandatory_fields):
                return True

        missing_headers = [header for count, header
                           in zip(mandatory_fields_counts,
                                  self.mandatory_fields)
                           if count == 0]
        duplicate_headers = [header for count, header
                             in zip(mandatory_fields_counts,
                                    self.mandatory_fields)
                             if count > 1]

        if missing_headers and duplicate_headers:
            raise ValueError(f"CSV bestand mist de volgende verplichte"
                             f" headers: {missing_headers}\n"
                             f"En heeft de volgende duplicate headers: "
                             f"{duplicate_headers}")
        if missing_headers:
            raise ValueError(f"CSV bestand mist de volgende verplichte"
                             f" headers: {missing_headers}")
        if duplicate_headers:
            raise ValueError(f"CSV bestand heeft de volgende duplicate"
                             f" headers: {duplicate_headers}")

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
            errors = []
            for row in reader:
                # Remove empty fields
                for key, value in row.items():
                    if (not isinstance(value, str) or value == "" or
                            value.isspace()):
                        row[key] = None
                try:
                    correct_date_format, file = self.generate_file(row, path,
                                                                   row_index)
                    yield file
                    if not correct_date_format:
                        errors.append(
                            SyntaxWarning(
                                f"De datum van document {row_index} kon niet "
                                f"worden geïnterpreteerd: '{row.get('date')}'."
                                f" Dit bestand is zonder datum ingeladen."))
                except Exception as e:
                    errors.append(e)
                row_index += 1

        if errors:
            if len(errors) == 1:
                raise errors[0]
            else:
                raise ExceptionGroup("Er zijn meerdere fouten opgetreden "
                                     "bij het laden van het bestand: ", errors)

    def generate_file(self, file: dict, path: str, row_index: int) -> (
            tuple[bool, RawFile]):
        """
        Generates a File object from a CSV row.

        :param file: A dictionary representing a row of CSV data.
        :param path: The string path to the CSV file.
        :param row_index: The index of the row in the csv file. Used for
        debugging and error presentation to the user.
        :return: A tuple of a boolean and a RawFile object. The boolean is
        False if the datetime could not be parsed, and True if the datetime
        was successfully parsed or if the datetime does not exist for that
        document. A RawFile object generated from the CSV row containing
        metadata and the raw text of the file.
        """
        for key in self.mandatory_fields:
            if file.get(key) is None:
                raise KeyError(f"De kolom '{key}' is verplicht, maar is niet "
                               f"gevonden voor document {row_index}")

        file_date_str: str = file.get("date")
        file_date: datetime
        correct_date_format: bool
        if file_date_str is None:
            file_date = None
            correct_date_format = True
        else:
            file_date = self.parse_date(file_date_str)
            correct_date_format = file_date is not None
        dict_title = file.get("title")
        alt_title = os.path.basename(path).replace('.csv', '')
        file_title = alt_title if dict_title is None else dict_title
        return correct_date_format, RawFile(
            metadata=Metadata(author=file.get("author"),
                              title=file_title, date=file_date,
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
