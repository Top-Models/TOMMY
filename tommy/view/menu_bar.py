from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMenuBar, QMenu, QWidget
from tommy.support.constant_variables import (
    prim_col_red, extra_light_gray, text_font)


class MenuBar(QMenuBar):
    """Menu bar class for the topic modelling application"""

    def __init__(self, parent: QWidget) -> None:
        """Initialize the menu bar."""
        super().__init__(parent)

        # Create actions
        import_input_folder_action = QAction("Selecteer input folder", self)
        export_action = QAction("Exporteren", self)

        # Create submenu for export
        export_to_gexf = QMenu(self)
        export_to_gexf.addAction("Graph Exchange XML Format (.gexf)")
        export_action.setMenu(export_to_gexf)

        # Connect actions to event handlers
        import_input_folder_action.triggered.connect(
            self.import_input_folder())
        export_to_gexf.triggered.connect(self.export_to_gexf())

        # Create menu bar
        file_menu = self.addMenu("Bestand")
        file_menu.addAction(import_input_folder_action)
        file_menu.addAction(export_action)

        # Set style
        self.setStyleSheet(f"""
            QMenuBar {{
                background-color: {prim_col_red};
                color: {extra_light_gray};
                font-family: {text_font};
            }}
            QMenuBar::item:selected {{
                background-color: {extra_light_gray};
                color: {prim_col_red};
            }}
            QMenuBar::item:pressed {{
                background-color: {extra_light_gray};
                color: {prim_col_red};
            }}
            QMenu {{
                background-color: {prim_col_red};
                color: {extra_light_gray};
            }}
            QMenu::item:selected {{
                background-color: {extra_light_gray};
                color: {prim_col_red};
            }}
        """)

    def import_input_folder(self) -> None:
        """
        Import a folder with input files.

        :return: None
        """
        pass

    def export_to_gexf(self) -> None:
        """
        Export the current graph to a GEXF file.

        :return: None
        """
        pass


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University 
(Department of Information and Computing Sciences)
"""
