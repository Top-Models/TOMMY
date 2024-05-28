from PySide6.QtWidgets import QMessageBox, QScrollArea, QWidget, QVBoxLayout, \
    QLabel


class ErrorView(QMessageBox):
    def __init__(self, error_description: str, errors: list[str], *args,
                 **kwargs):
        QMessageBox.__init__(self, *args, **kwargs)
        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)
        self.content = QWidget()
        description = QLabel(error_description, self)
        self.layout().addWidget(description)
        scroll.setWidget(self.content)
        lay = QVBoxLayout(self.content)
        for error in errors:
            lay.addWidget(QLabel(error, self))
        self.layout().addWidget(scroll)
        self.setStyleSheet("QScrollArea{min-width:300 px; min-height: 200px}")
        self.exec_()
