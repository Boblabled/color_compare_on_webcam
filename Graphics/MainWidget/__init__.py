from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QAction

from Graphics.MainWidget import ui_main
from Graphics import CameraWidget, TimerWidget, ToolsWidget
from Graphics.LoggerWidget import Widget as LoggerWidget
from Graphics.CameraWidget import Widget as CameraWidget
from Graphics.TimerWidget import Widget as TimerWidget
from Graphics.ToolsWidget import Widget as ToolsWidget
from Service import convertui
from Workers.memory_keys import Workers

convertui.convertui(__file__, 'ui_main')


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, workers_memory, threads_memory):
        super().__init__()
        self.__workers_memory = workers_memory
        self.mainWidget = Widget(workers_memory, threads_memory)
        self.setCentralWidget(self.mainWidget)
        self.resize(836, 800)
        view_menu = self.menuBar().addMenu('Вид')

        logger_action = QAction('Логгер', self, checkable=True)
        logger_action.triggered.connect(self.showLogger)
        view_menu.addAction(logger_action)

        tool_action = QAction('Панель управления', self, checkable=True)
        tool_action.triggered.connect(self.showTools)
        view_menu.addAction(tool_action)

        with open("Graphics/Styles/styles.css", "r") as file:
            self.setStyleSheet(file.read())

    def showLogger(self, checked):
        if checked:
            self.mainWidget.logger_widget.show()
        else:
            self.mainWidget.logger_widget.hide()

    def showTools(self, checked):
        if checked:
            self.mainWidget.tools_widget.show()
            self.__workers_memory[Workers.amperage_sensors_worker].resume()
        else:
            self.mainWidget.tools_widget.hide()
            self.__workers_memory[Workers.amperage_sensors_worker].pause()


class Widget(QtWidgets.QWidget, ui_main.Ui_WidgetName):
    stop_workers = pyqtSignal()

    def __init__(self, workers_memory, threads_memory, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)
        self.__workers_memory = workers_memory
        self.__threads_memory = threads_memory

        self.verticalLayout.addWidget(CameraWidget(self.__workers_memory))
        self.verticalLayout.addWidget(TimerWidget(self.__workers_memory))

        self.logger_widget = LoggerWidget()
        self.verticalLayout.addWidget(self.logger_widget)
        self.logger_widget.hide()

        self.tools_widget = ToolsWidget(self.__workers_memory)

        for worker in self.__workers_memory.keys():
            worker: str
            self.stop_workers.connect(self.__workers_memory[worker].stop)
            self.__workers_memory[worker].stopped_signal.connect(self.__threads_memory[worker].quit)

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        self.stop_workers.emit()
        return super().closeEvent(event)
