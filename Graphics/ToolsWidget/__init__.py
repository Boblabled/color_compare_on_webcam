import logging

from PyQt5 import QtWidgets, QtGui
from PyQt5.uic.properties import QtCore
from serial.serialutil import SerialException

from Graphics.ToolsWidget import ui_tools
from Modules.request_manager import RequestManager
from Service import convertui
from Workers.memory_keys import Workers

convertui.convertui(__file__, 'ui_tools')


# TODO разбить на подмодули
class Widget(QtWidgets.QWidget, ui_tools.Ui_Form):
    def __init__(self, workers_memory, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)
        self.__workers_memory = workers_memory
        self.request_manager = None
        try:
            self.request_manager = RequestManager("1", 9600, 8)
        except SerialException:
            logging.critical("Невозможно подключиться к порту")

        with open("Graphics/Styles/styles.css", "r") as file:
            self.setStyleSheet(file.read())

        self.__off_lock_state = False
        self.__auto_work_state = False
        self.__tambur_light = 0
        self.__room_light = 0
        self.__tambur_unlock = False
        self.__room_unlock = False
        self.__spin_box_period = 0
        self.__spin_box_time = 0
        self.__spin_box_limit = 0
        self.__fan_mode = [0, 0]
        # TODO установить через реквест
        self.__shutter_pos = [0, 0]
        self.__light_panel_mode = 0

        self.sliderFan1.valueChanged.connect(lambda value: self.setLabelInfo(value, self.labelFanSpeed1))
        self.sliderFan2.valueChanged.connect(lambda value: self.setLabelInfo(value, self.labelFanSpeed2))
        self.sliderShutter1.valueChanged.connect(lambda value: self.setLabelInfo(value, self.labelShutterPos1))
        self.sliderShutter2.valueChanged.connect(lambda value: self.setLabelInfo(value, self.labelShutterPos2))
        self.applyButton.clicked.connect(self.setSettings)

        self.__workers_memory[Workers.amperage_sensors_worker].connect(self.setAmperageFromSensors, 100)

    def setSettings(self) -> None:
        if self.request_manager is not None:
            # чекбоксы
            self.setOffLock(self.checkBoxOffLock.isChecked())
            self.startAutoWork(self.checkBoxAutoWork.isChecked())
            self.setTamburLight(self.checkBoxTamburLight.isChecked())
            self.setRoomLight(self.checkBoxRoomLight.isChecked())
            self.setTamburUnlock(self.checkBoxLockTambur.isChecked())
            self.setRoomUnlock(self.checkBoxLockRoom.isChecked())

            # спинбоксы
            # TODO возможно могут быть None
            self.setPeriodOn(self.spinBoxPeriod.value())
            self.setLimitOn(self.spinBoxLimit.value())
            self.setTimeOn(self.spinBoxTime.value())

            # слайдеры
            self.setFanSpeed(1, self.sliderFan1.value())
            self.setFanSpeed(2, self.sliderFan2.value())
            self.setShutterPos(1, self.sliderShutter1.value())
            self.setShutterPos(2, self.sliderShutter2.value())

            # комбобоксы
            self.setLightPanel(self.comboBoxLight.currentIndex())

        else:
            logging.error("Нет подключения")

    def setOffLock(self, state: bool) -> None:
        if state != self.__off_lock_state:
            self.__off_lock_state = state
            if self.__off_lock_state:
                self.request_manager.setBlockEmergencyOff()
            else:
                self.request_manager.stopBlockEmergencyOffThread()

    def startAutoWork(self, state: bool) -> None:
        if state != self.__auto_work_state:
            self.__auto_work_state = state
            if self.__auto_work_state:
                self.request_manager.setOpenAllow()
            else:
                logging.debug("Надо как-то отключать")

    def setTamburLight(self, state: int) -> None:
        if state != self.__tambur_light:
            self.__tambur_light = state
            self.request_manager.setLightning(int(self.__tambur_light), int(self.__room_light))

    def setRoomLight(self, state: int) -> None:
        if state != self.__room_light:
            self.__room_light = state
            self.request_manager.setLightning(int(self.__tambur_light), int(self.__room_light))

    def setTamburUnlock(self, state: bool) -> None:
        if state != self.__tambur_unlock:
            if state:
                if self.request_manager.doorThreadStatusRun():
                    self.request_manager.stopDoorLockThread()
                self.__tambur_unlock = True
                self.request_manager.setDoorLock(tambur=self.__tambur_unlock, room=self.__room_unlock)
            else:
                self.__tambur_unlock = False
                if self.request_manager.doorThreadStatusRun():
                    self.request_manager.stopDoorLockThread()

    def setRoomUnlock(self, state: bool) -> None:
        if state != self.__room_unlock:
            if state:
                if self.request_manager.doorThreadStatusRun():
                    self.request_manager.stopDoorLockThread()
                self.__room_unlock = True
                self.request_manager.setDoorLock(tambur=self.__tambur_unlock, room=self.__room_unlock)
            else:
                self.__room_unlock = False
                if self.request_manager.doorThreadStatusRun():
                    self.request_manager.stopDoorLockThread()

    def setPeriodOn(self, period: int) -> None:
        if period != self.__spin_box_period:
            self.__spin_box_period = period
            self.request_manager.setPeriodOn(self.__spin_box_period)

    def setTimeOn(self, time: int) -> None:
        if time != self.__spin_box_period:
            self.__spin_box_time = time
            self.request_manager.setPeriodOn(self.__spin_box_time)

    def setLimitOn(self, limit: int) -> None:
        if limit != self.__spin_box_limit:
            self.__spin_box_limit = limit
            self.request_manager.setPeriodOn(self.__spin_box_limit)

    def setFanSpeed(self, fan: int, mode: int) -> None:
        if mode != self.__fan_mode[fan-1]:
            self.__fan_mode[fan-1] = mode
            self.request_manager.setFanSpeed(fan, self.__fan_mode[fan-1])

    def setShutterPos(self, shutter: int, pos: int) -> None:
        if pos != self.__fan_mode[shutter-1]:
            self.__shutter_pos[shutter-1] = pos
            self.request_manager.setOpenShutter(shutter, self.__shutter_pos[shutter-1])

    def setLightPanel(self, mode: int) -> None:
        if mode != self.__light_panel_mode:
            self.__light_panel_mode = mode
            self.request_manager.setLight(mode)

    def setAmperageFromSensors(self) -> None:
        if self.request_manager is not None:
            self.lcdNumber.setText(str(self.request_manager.getI(1, amper=True)))
            self.lcdNumber_2.setText(str(self.request_manager.getI(2, amper=True)))
            self.lcdNumber_3.setText(str(self.request_manager.getI(3, amper=True)))
            self.lcdNumber_4.setText(str(self.request_manager.getI(4, amper=True)))
            self.lcdNumber_5.setText(str(self.request_manager.getI(5, amper=True)))
        else:
            logging.error("Нет подключения")

    def setLabelInfo(self, value: int, label: QtWidgets.QLabel) -> None:
        label.setText(str(value))

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        self.__workers_memory[Workers.amperage_sensors_worker].pause()
        return super().closeEvent(event)
