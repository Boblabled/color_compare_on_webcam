from PyQt5 import QtWidgets
from PyQt5.QtCore import QTimer

from Graphics.TimerWidget import ui_timer
from Service import convertui
from Workers.memory_keys import Workers

convertui.convertui(__file__, 'ui_timer')


class Widget(QtWidgets.QWidget, ui_timer.Ui_Form):
    def __init__(self, workers_memory, parent=None):
        super().__init__(parent=parent)
        self.__workers_memory = workers_memory
        self.setupUi(self)
        self.__timer_flag = False
        self.__time = 0

        self.__workers_memory[Workers.timer_worker].connect(self.showTime)
        self.start_button.pressed.connect(self.start)
        self.stop_button.pressed.connect(self.stop)
        self.reset_button.pressed.connect(self.reset)

    def showTime(self):
        if self.__timer_flag:
            self.__time += 1
        self.lcd_timer.display("%02d:%02d:%02d" % (self.__time // 1200, self.__time % 1200 // 60, self.__time % 60))

    def start(self):
        self.__timer_flag = True

    def stop(self):
        self.__timer_flag = False

    def reset(self):
        self.__timer_flag = False
        self.__time = 0
        self.lcd_timer.display("00:00:00")
