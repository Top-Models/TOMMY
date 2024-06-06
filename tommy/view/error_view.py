from PySide6.QtWidgets import QMessageBox, QScrollArea, QWidget, QVBoxLayout, \
    QLabel

from tommy.support.constant_variables import heading_font, text_font, \
    prim_col_red, seco_col_blue, hover_seco_col_blue, pressed_seco_col_blue


class ErrorView(QMessageBox):
    """
    The error view class is responsible for displaying
    error messages to the user.
    """

    def __init__(self, error_description: str, errors: list[str], *args,
                 **kwargs):
        """Create a new error popup"""
        super().__init__(*args, **kwargs)

        # Initialize window properties
        self.setWindowTitle("Error")
        self.setStyleSheet(f"""
            QMessageBox {{
                background-color: white;
            }}
            
            QPushButton {{
                font-size: 15px;
                font-family: {text_font};
                color: white;
                border: none;
                padding: 10px;
                background-color: {seco_col_blue};
            }}
            
            QPushButton:hover {{
                background-color: {hover_seco_col_blue};
            }}
            
            QPushButton:pressed {{
                background-color: {pressed_seco_col_blue};
            }}
        """)

        # Create a QWidget to hold the custom layout
        custom_widget = QWidget()
        custom_layout = QVBoxLayout(custom_widget)

        # Create title label
        title_label = QLabel("ERROR")
        title_label.setStyleSheet(f"""
            font-family: '{heading_font}', sans-serif;
            font-size: 20px;
            color: {prim_col_red};
        """)
        custom_layout.addWidget(title_label)

        # Create label with error description
        error_description_label = QLabel(error_description)
        error_description_label.setWordWrap(True)
        error_description_label.setMaximumWidth(400)
        error_description_label.setStyleSheet(f"""
            font-family: '{text_font}', sans-serif;
            font-size: 16px;
            color: black;
        """)
        custom_layout.addWidget(error_description_label)

        # Optionally add a list of errors (if provided)
        if errors:
            for error in errors:
                error_label = QLabel(f"• {error}")
                error_label.setWordWrap(True)
                error_label.setMaximumWidth(400)
                error_label.setStyleSheet(f"""
                    font-family: '{text_font}', sans-serif;
                    font-size: 14px;
                    color: black;
                    margin-bottom: 5px;
                """)
                custom_layout.addWidget(error_label)

        # Create a scroll area to hold the custom widget
        scroll_area = QScrollArea()
        scroll_area.setWidget(custom_widget)
        scroll_area.setWidgetResizable(True)
        scroll_area.setMinimumWidth(400)
        scroll_area.setMinimumHeight(200)
        scroll_area.setStyleSheet(f"""
            border: none;
            background-color: white;
        """)

        # Add the scroll area to the message box layout
        self.layout().addWidget(scroll_area, 0, 0, 1,
                                self.layout().columnCount())

        # Display the message box
        self.exec()


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University
(Department of Information and Computing Sciences)
"""
