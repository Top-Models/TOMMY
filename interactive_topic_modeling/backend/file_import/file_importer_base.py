from abc import ABC, abstractmethod
from datetime import date, datetime
from dateutil import parser


class FileImporterBase(ABC):

    @abstractmethod
    def load_file(self, path: str) -> str:
        pass

    @abstractmethod
    def compatible_file(self, path: str) -> bool:
        pass

    def parse_date(self, file_date: str) -> date:
        parse_info = DutchParseInfo()
        return parser.parse(file_date, parserinfo=parse_info).date()


class DutchParseInfo(parser.parserinfo):
    def __init__(self):
        super().__init__(dayfirst=True)
        self.MONTHS = [('January', 'Januari', 'Jan', 'Jan.'),
                       ('February', 'Februari', 'Feb', 'Feb.', 'Febr', 'Febr.'),
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
                         ('Wed', 'Wednesday', 'Woensdag', 'Wo', 'Wo.', 'Woe', 'Woe.'),
                         ('Thu', 'Thursday', 'Donderdag', 'Do', 'Do.'),
                         ('Fri', 'Friday', 'Vrijdag', 'Vr', 'Vr.', 'Vrij', 'Vrij.'),
                         ('Sat', 'Saturday', 'Zaterdag', 'Za', 'Za.', 'Zat', 'Zat.'),
                         ('Sun', 'Sunday', 'Zondag', 'Zo', 'Zo.')]
