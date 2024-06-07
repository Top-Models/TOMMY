from typing import Any

from PySide6.QtCore import Qt, QRect, QPoint, QSize, QTimer
from PySide6.QtWidgets import QSizePolicy, QLayout, QLayoutItem


class FlowLayout(QLayout):
    def __init__(self, parent=None, margin=5, spacing=0):
        super().__init__(parent)

        if parent is not None:
            self.setContentsMargins(15, margin, margin, margin)

        # Make content align center
        self.setAlignment(Qt.AlignmentFlag.AlignCenter |
                          Qt.AlignmentFlag.AlignTop)

        self.setSpacing(spacing)
        self.itemList = []

    def addItem(self, item: QLayoutItem) -> None:
        """
        Add an item to the layout

        :param item: The item to add
        :return: None
        """
        self.itemList.append(item)

    def count(self) -> int:
        """
        Get the number of items in the layout

        :return: The number of items in the layout
        """
        return len(self.itemList)

    def itemAt(self, index: int) -> QLayoutItem | None:
        """
        Get the item at the given index

        :param index: The index of the item
        :return: The item at the given index
        """
        if 0 <= index < len(self.itemList):
            return self.itemList[index]

        return None

    def takeAt(self, index: int) -> QLayoutItem | None:
        """
        Remove the item at the given index

        :param index: The index of the item to remove
        :return: The item that was removed
        """
        if 0 <= index < len(self.itemList):
            return self.itemList.pop(index)

        return None

    def expandingDirections(self) -> Qt.Orientations:
        """
        Get the expanding directions of the layout

        :return: The expanding directions of the layout
        """
        return Qt.Orientations(Qt.Orientation(0))

    def hasHeightForWidth(self) -> bool:
        """
        Check if the layout has a height for width

        :return: True if the layout has a height for width,
        False otherwise
        """
        return True

    def heightForWidth(self, width: int) -> int:
        """
        Get the height for the given width

        :param width: The width to get the height for
        :return: The height for the given width
        """
        return self.do_layout(QRect(0, 0, width, 0), True)

    def setGeometry(self, rect: QRect) -> None:
        """
        Set the geometry of the layout

        :param rect: The rectangle to set the geometry to
        :return: None
        """
        super().setGeometry(rect)
        self.do_layout(rect, False)

    def sizeHint(self) -> QSize:
        """
        Get the size hint of the layout

        :return: The size hint of the layout
        """
        return self.minimumSize()

    def minimumSize(self) -> QSize:
        """
        Get the minimum size of the layout

        :return: The minimum size of the layout
        """
        size = QSize()

        for item in self.itemList:
            size = size.expandedTo(item.minimumSize())

        margin = self.contentsMargins().left()
        size += QSize(2 * margin, 2 * margin)
        return size

    def do_layout(self, rect: QRect, test_only: bool) -> int:
        """
        Perform the layout

        :param rect: The rectangle to perform the layout in
        :param test_only: True if the layout should only be tested,
        False otherwise
        :return: The height of the layout
        """
        x = rect.x() + self.contentsMargins().left()
        y = rect.y() + self.contentsMargins().top()
        line_height = 0
        space_y = self.spacing()

        # Add a constant margin of 15px to the right
        right_margin = 15

        # Add a reduction margin to make items take less space artificially
        reduction_margin = 80

        # Calculate items per line
        items_per_line = []
        current_line = []
        line_width = 0

        for item in self.itemList:
            wid = item.widget()
            if not wid:
                continue

            style = wid.style() if hasattr(wid, 'style') else None
            space_x = self.spacing()
            space_y = self.spacing()

            if style:
                try:
                    space_x += style.layoutSpacing(
                        QSizePolicy.PushButton, QSizePolicy.PushButton,
                        Qt.Horizontal)
                    space_y += style.layoutSpacing(
                        QSizePolicy.PushButton, QSizePolicy.PushButton,
                        Qt.Vertical)
                except AttributeError:
                    pass

            # Calculate the width including the right margin and reduction
            # margin
            item_width = (wid.sizeHint().width() + right_margin -
                          reduction_margin)

            next_x = x + item_width + space_x
            if next_x - space_x > rect.right() and line_height > 0:
                items_per_line.append((current_line, line_width))
                current_line = []
                x = rect.x() + self.contentsMargins().left()
                y = y + line_height + space_y
                next_x = x + item_width + space_x
                line_height = 0
                line_width = 0

            current_line.append(item)
            x = next_x
            line_height = max(line_height, wid.sizeHint().height())
            line_width += item_width + space_x

        items_per_line.append((current_line, line_width))

        # Reset x and y for actual layout
        x = rect.x() + self.contentsMargins().left()
        y = rect.y() + self.contentsMargins().top()
        line_height = 0

        # Perform actual layout
        for line, line_width in items_per_line:
            extra_space = rect.width() - line_width + self.spacing()
            extra_space_per_item = extra_space // max(1, len(line))

            for idx, item in enumerate(line):
                wid = item.widget()
                if not wid:
                    continue

                style = wid.style() if hasattr(wid, 'style') else None
                space_x = self.spacing()
                space_y = self.spacing()

                if style:
                    try:
                        space_x += style.layoutSpacing(
                            QSizePolicy.PushButton, QSizePolicy.PushButton,
                            Qt.Horizontal)
                        space_y += style.layoutSpacing(
                            QSizePolicy.PushButton, QSizePolicy.PushButton,
                            Qt.Vertical)
                    except AttributeError:
                        pass

                # Adjust width based on whether it's the last item in the line
                if idx == len(line) - 1:
                    item_width = (wid.sizeHint().width() + extra_space_per_item
                                  - reduction_margin)
                else:
                    item_width = (wid.sizeHint().width() + extra_space_per_item
                                  + right_margin - reduction_margin)

                if not test_only:
                    item.setGeometry(QRect(QPoint(x, y),
                                           QSize(item_width,
                                                 wid.sizeHint().height())))

                x += item_width + space_x
                line_height = max(line_height, wid.sizeHint().height())

            x = rect.x() + self.contentsMargins().left()
            y += line_height + space_y
            line_height = 0

        # Update the layout
        QTimer.singleShot(0, self.update)
        return y + line_height - rect.y()


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University
(Department of Information and Computing Sciences)
"""