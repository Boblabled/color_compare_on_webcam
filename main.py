import sys
from PyQt5.QtWidgets import QApplication
from PyQt5 import QtCore, QtWidgets

import widget

application = QApplication(sys.argv)


class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setGeometry(QtCore.QRect(100, 100, 418, 400))
        self.setWindowTitle('Сравнение цветовых гамм в области')

        # Основа всего приложения
        self.main_widget = QtWidgets.QWidget(self)

        self.main_layout = QtWidgets.QHBoxLayout(self.main_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        # Добавление виджетов

        self.demo_widget = widget.Widget(parent=self.main_widget)

        # Завершение настройки

        self.main_layout.addWidget(self.demo_widget)
        self.setCentralWidget(self.main_widget)


application_window = ApplicationWindow()
application_window.show()
application.exec()
sys.exit()
