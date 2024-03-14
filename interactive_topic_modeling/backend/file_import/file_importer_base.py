from abc import ABC, abstractmethod
from datetime import date
from dateutil import parser
from typing import Generator

from interactive_topic_modeling.backend.file_import.file import File


class FileImporterBase(ABC):
    """
    Abstract base class for file importers.
    """
    @abstractmethod
    def load_file(self, path: str) -> Generator[File, None, None]:
        """
        Abstract method to load a file.

        :param path: The string path of the file.
        :return Generator[File, None, None]: A generator yielding File objects.
        """
        pass

    @abstractmethod
    def compatible_file(self, path: str) -> bool:
        """
        Abstract method to check if a file is compatible.

        :param path: The path to the file.
        :return bool: True is compatible, False otherwise.
        """
        pass

    def parse_date(self, file_date: str) -> date:
        """
        Parse the Dutch date string into a date object.

        :param file_date: The date string to parse.
        :return date: The date object .
        """
        parse_info = DutchParseInfo()
        return parser.parse(file_date, parserinfo=parse_info, fuzzy=True,
                            dayfirst=True).date()


class DutchParseInfo(parser.parserinfo):
    """
    Dutch date information to parse dates.
    """
    def __init__(self):
        """
        The initialization of the DutchParseInfo object.
        """
        self.MONTHS = [('January', 'Januari', 'Jan', 'Jan.'),
                       ('February', 'Februari', 'Feb', 'Feb.', 'Febr',
                        'Febr.'),
                       ('March', 'Maart', 'Mrt', 'Mrt.', 'Mar', 'Mar.'),
                       ('April', 'Apr', 'Apr.'),
                       ('May', 'Mei'),
                       ('June', 'Juni', 'Jun', 'Jun.'),
                       ('July', 'Juli', 'Jul', 'Jul.'),
                       ('August', 'Augustus', 'Aug', 'Aug.'),
                       ('September', 'Sep', 'Sep.', 'Sept', 'Sept.'),
                       ('October', 'Oktober', 'Okt', 'Okt.', 'Oct', 'Oct.'),
                       ('November', 'Nov', 'Nov.'),
                       ('December', 'Dec', 'Dec.')]

        self.WEEKDAYS = [('Mon', 'Monday', 'Maandag', 'Ma', 'Ma.'),
                         ('Tue', 'Tuesday', 'Dinsdag', 'Di', 'Di.'),
                         ('Wed', 'Wednesday', 'Woensdag', 'Wo', 'Wo.',
                          'Woe', 'Woe.'),
                         ('Thu', 'Thursday', 'Donderdag', 'Do', 'Do.'),
                         ('Fri', 'Friday', 'Vrijdag', 'Vr', 'Vr.', 'Vrij',
                          'Vrij.'),
                         ('Sat', 'Saturday', 'Zaterdag', 'Za', 'Za.', 'Zat',
                          'Zat.'),
                         ('Sun', 'Sunday', 'Zondag', 'Zo', 'Zo.')]

        super().__init__(dayfirst=True)


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University 
(Department of Information and Computing Sciences)
"""
