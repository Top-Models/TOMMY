import logging

from PySide6.QtCore import Qt, QRect, QSize, QPoint
from PySide6.QtWidgets import QLayout, QLayoutItem

logging.basicConfig(level=logging.DEBUG)


class FlowLayout(QLayout):
    def __init__(self, parent=None, margin=5, spacing=10):
        super().__init__(parent)

        if parent is not None:
            self.setContentsMargins(10, margin, 10, margin)

        # Make content align center
        self.setAlignment(
            Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)

        self.setSpacing(spacing)
        self.itemList = []

    def addItem(self, item: QLayoutItem) -> None:
        self.itemList.append(item)

    def count(self) -> int:
        return len(self.itemList)

    def itemAt(self, index: int) -> QLayoutItem | None:
        if 0 <= index < len(self.itemList):
            return self.itemList[index]
        return None

    def takeAt(self, index: int) -> QLayoutItem | None:
        if 0 <= index < len(self.itemList):
            return self.itemList.pop(index)
        return None

    def expandingDirections(self) -> Qt.Orientations:
        return Qt.Orientations(Qt.Orientation(0))

    def hasHeightForWidth(self) -> bool:
        return True

    def heightForWidth(self, width: int) -> int:
        return self.do_layout(QRect(0, 0, width, 0), True)

    def setGeometry(self, rect: QRect) -> None:
        super().setGeometry(rect)
        self.do_layout(rect, False)

    def sizeHint(self) -> QSize:
        return self.minimumSize()

    def minimumSize(self) -> QSize:
        size = QSize()
        for item in self.itemList:
            size = size.expandedTo(item.minimumSize())
        margin = self.contentsMargins().left()
        size += QSize(2 * margin, 2 * margin)
        return size

    def do_layout(self, rect: QRect, test_only: bool) -> int:
        x = rect.x() + self.contentsMargins().left()
        y = rect.y() + self.contentsMargins().top()
        line_height = 0
        space_y = self.spacing()

        # Calculate items per line
        items_per_line = []
        current_line = []
        line_width = 0

        for item in self.itemList:
            wid = item.widget()
            if not wid:
                continue

            item_width = wid.sizeHint().width()
            item_height = wid.sizeHint().height()
            space_x = self.spacing()

            next_x = x + item_width + space_x
            if (next_x - space_x > rect.right() -
                    self.contentsMargins().right() and line_height > 0):
                items_per_line.append((current_line, line_width))
                current_line = []
                x = rect.x() + self.contentsMargins().left()
                y += line_height + space_y
                next_x = x + item_width + space_x
                line_height = 0
                line_width = 0

            current_line.append(item)
            x = next_x
            line_height = max(line_height, item_height)
            line_width += item_width + space_x

        items_per_line.append((current_line, line_width))

        # Reset x and y for actual layout
        x = rect.x() + self.contentsMargins().left()
        y = rect.y() + self.contentsMargins().top()
        line_height = 0

        for line, line_width in items_per_line:
            extra_space = (rect.width() - line_width -
                           self.contentsMargins().right())
            extra_space_per_item = extra_space // max(1, len(line))

            for idx, item in enumerate(line):
                wid = item.widget()
                if not wid:
                    continue

                space_x = self.spacing()
                item_width = wid.sizeHint().width() + extra_space_per_item
                item_height = wid.sizeHint().height()

                if not test_only:
                    logging.debug(
                        f"Setting geometry for item: x={x}, y={y}, "
                        f"width={item_width}, height={item_height}")
                    item.setGeometry(
                        QRect(QPoint(x, y), QSize(item_width, item_height)))

                x += item_width + space_x
                line_height = max(line_height, item_height)

            x = rect.x() + self.contentsMargins().left()
            y += line_height + space_y
            line_height = 0

        return y + line_height - rect.y()


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University
(Department of Information and Computing Sciences)
"""
