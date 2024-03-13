import time
import logging
import serial

from enum import Enum
from modbus_tk import modbus_rtu
from threading import Thread

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


class Command(Enum):
    READ_COIL_STATUS = 0x01  # чтение DO - дискретный
    READ_INPUT_STATUS = 0x02  # чтение DI - дискретный
    READ_HOLDING_REGISTER = 0x03  # чтение AO - 16 битное
    READ_INPUT_REGISTER = 0x04  # чтение AI - 16 битное
    FORCE_SINGLE_POINT = 0x05  # запись одного DO - дискретный
    PRESENT_SINGLE_REGISTER = 0x06  # запись одного AO - 16 битное
    FORCE_MULTIPLE_COILS = 0x07  # запись нескольких DO - дискретный
    PRESENT_MULTIPLE_REGISTER = 0x08  # запись нескольких AO - 16 битное


class RequestManager:
    __slave = 1

    def __init__(self, port: str, baudrate: int, bytesize: int):
        self.master = modbus_rtu.RtuMaster(
            serial.Serial(port=port, baudrate=baudrate, bytesize=bytesize, parity='N', stopbits=1, xonxoff=0))
        self.master.set_timeout(0.5)
        self.master.set_verbose(True)

        self.__door_lock_thread_status = False
        self.__stop_block_emergency_off = False
        self.__stop_door_lock = False

    def getVersion(self) -> int:
        """Версия встроенного программного обеспечения устройства (начиная с 1)"""
        return self.master.execute(self.__slave, Command.READ_INPUT_REGISTER, 1)

    def setPeriodOn(self, period: int) -> None:
        """Период включения клапана хлора в мс. Значение в данном регистре должно
        изменяться только при отключенном клапане подачи хлора"""
        # TODO а как определить что клапан отключен???
        self.master.execute(self.__slave, Command.PRESENT_SINGLE_REGISTER, 2, output_value=period)

    def setTimeOn(self, time: int) -> None:
        """Время включения клапана хлора в каждом периоде в мс. Значение в
        данном регистре должно изменяться только при отключенном клапане подачи хлора"""
        self.master.execute(self.__slave, Command.PRESENT_SINGLE_REGISTER, 3, output_value=time)

    def setLimitOn(self, limit: int, amper=True) -> None:
        """Уставка порога включения клапана по хлору (в сотых долях тока от
        диапазона измерений анализатора хлора, 1мА = 100 единиц)"""
        koeff = 1
        if amper:
            koeff = 100
        self.master.execute(self.__slave, Command.PRESENT_SINGLE_REGISTER, 4, output_value=limit * koeff)

    def getI(self, channel: int, amper=True) -> int:
        """Измеренное значение тока канала датчика концентрации хлора channel(1-4), 1мА = 100 единиц)"""
        START_ADDRESS = 4
        if channel < 1 or channel > 4:
            logging.debug("Channel must be between 1 and 4")
            return -1
        elif amper:
            return self.master.execute(self.__slave, Command.READ_INPUT_REGISTER, START_ADDRESS + channel) / 100
        else:
            return self.master.execute(self.__slave, Command.READ_INPUT_REGISTER, START_ADDRESS + channel)

    def getAverageI(self, amper=True) -> int:
        """Среднее значение тока по всем каналам датчиков концентрации хлора, 1мА = 100 единиц)"""
        if amper:
            return self.master.execute(self.__slave, Command.READ_INPUT_REGISTER, 9) / 100
        else:
            return self.master.execute(self.__slave, Command.READ_INPUT_REGISTER, 9)

    def setOpenAllow(self) -> None:
        """Разрешение работы (открытия) клапана подачи хлора.
        Бит 0 – разрешение автоматического управления клапаном хлора по показаниям датчиков концентрации"""
        # TODO почему только один режим, как его потом выключить?
        self.master.execute(self.__slave, Command.PRESENT_SINGLE_REGISTER, 10, output_value=0)

    def setBlockEmergencyOff(self) -> None:
        """Регистр блокировки аварийного отключения клапана подачи хлора по таймауту.
        Регистр предназначен для отключения блокировки аварийного отключения клапана подачи хлора по таймауту.
        Для отключения блокировки, программное обеспечение верхнего уровня должно, не реже 1 раза в 15 секунд,
        последовательно записывать в данный регистр значения 0 и 1. Временной промежуток между записями значений
        должен быть не менее 0,5 сек."""
        # TODO похоже на говно
        self.__stop_block_emergency_off = False
        thread = Thread(target=self.block_emergency_off, args=(lambda: self.__stop_block_emergency_off,))
        thread.start()

    def stopBlockEmergencyOffThread(self) -> None:
        self.__stop_block_emergency_off = True

    def blockEmergencyOff(self, stop) -> None:
        while True:
            self.master.execute(self.__slave, Command.PRESENT_SINGLE_REGISTER, 11, output_value=0)
            time.sleep(0.5)
            self.master.execute(self.__slave, Command.PRESENT_SINGLE_REGISTER, 11, output_value=1)
            time.sleep(14.5)
            if stop:
                break

    def setOpenShutter(self, shutter: int, pos: int) -> None:
        """Управление положением воздушной заслонки 1 или 2
        Значение 0 соответствует полностью открытому состоянию Значение 1000 соответствует полностью закрытому
        состоянию. Допускается указывать значения от 0 до 10000"""
        if 1 <= shutter <= 2:
            if 0 <= pos <= 10000:
                self.master.execute(self.__slave, Command.PRESENT_SINGLE_REGISTER, 12, output_value=pos)
            else:
                logging.debug("pos must be between 1 and 1000")
        else:
            logging.debug("shutter must be 1 or 2")

    def getShutterCurrentPos(self, shutter: int) -> int:
        """Текущее положение воздушной заслонки 1 или 2 (чтение показаний датчика положения заслонки)
        Значение 0 соответствует полностью открытому состоянию Значение 1000 соответствует полностью закрытому
        состоянию. Допускается указывать значения от 0 до 10000"""
        START_ADDRESS = 13
        if shutter < 1 or shutter > 2:
            return -1
        else:
            return self.master.execute(self.__slave, Command.READ_INPUT_REGISTER, START_ADDRESS + shutter)

    def setFanSpeed(self, fan: int, mode: int) -> None:
        """Управление вентилятором 1 или 2
        0 – малая скорость
        1 – средняя скорость
        2 – высокая скорость
        3 – вентилятор выключен"""
        START_ADDRESS = 15
        if 1 <= fan <= 2:
            if 0 <= mode <= 3:
                self.master.execute(self.__slave, Command.PRESENT_SINGLE_REGISTER, START_ADDRESS + fan, output_value=mode)
            else:
                logging.debug("mode must be between 1 and 3")
        else:
            logging.debug("fan must be between 1 and 3")

    def setLightning(self, tambur, room) -> None:
        """Управление освещением
        Бит 0 (инверсный):
        0 – освещение тамбура включено
        1 – освещение тамбура выключено
        Бит 1 (инверсный):
        0 – освещение камеры включено
        1 – освещение камеры выключено"""
        if 0 <= tambur <= 1:
            if 0 <= room <= 1:
                self.master.execute(self.__slave, Command.PRESENT_MULTIPLE_REGISTER, 18,
                                    output_value=[tambur, room])
            else:
                logging.debug("camera must be 0 or 1")
        else:
            logging.debug("tambur must be 0 or 1")

    def getSensorsStates(self):
        """Состояние кнопок открытия и датчиков открытия дверей
        Бит 0: состояние кнопки открытия двери тамбура
        0 – кнопка отпущена
        1 – кнопка нажата
        Бит 1: состояние кнопки открытия двери камеры
        0 – кнопка отпущена
        1 – кнопка нажата
        Бит 2: состояние двери тамбура
        0 – дверь открыта
        1 – дверь закрыта
        Бит 3: состояние двери камеры
        0 – дверь открыта
        1 – дверь закрыта"""
        keys = ("tambur_button", "room_button", "tambur_door", "room_door")
        status = self.master.execute(self.__slave, Command.READ_INPUT_REGISTER, 19)
        return {key: value for key, value in zip(keys, status)}

    def setDoorLock(self, tambur=True, room=True) -> None:
        """Управление электромагнитными замками дверей
        Бит 0: управление замком тамбура
        Бит 1: управление замком камеры
        Для снятия напряжения с электромагнитного замка двери, программное обеспечение верхнего уровня должно,
        не реже 1 раза в 7 секунд, последовательно записывать в соответствующий бит значений 0 и 1.
        Временной промежуток между записями значений должен быть не менее 0,1 сек."""
        self.__stop_door_lock = False
        if tambur or room:
            thread = Thread(target=self.door_lock, args=(tambur, room, lambda: self.__stop_door_lock))
            thread.start()
        else:
            logging.debug("Оба аргумента False")

    def doorThreadStatusRun(self) -> bool:
        return not self.__stop_door_lock

    def stopDoorLockThread(self) -> None:
        self.__stop_door_lock = True

    def doorLock(self, tambur, room, stop) -> None:
        while True:
            output_1 = [0, 1]
            output_2 = [1, 1]
            if tambur and room:
                output_1 = [0, 0]
                output_2 = [1, 1]
            elif not tambur and room:
                output_1 = [1, 0]
                output_2 = [1, 1]
            self.master.execute(self.__slave, Command.PRESENT_MULTIPLE_REGISTER, 20, output_value=output_1)
            time.sleep(0.5)
            self.master.execute(self.__slave, Command.PRESENT_MULTIPLE_REGISTER, 20, output_value=output_2)
            time.sleep(6.5)
            if stop:
                break

    def setLight(self, mode: int) -> None:
        """Управление световым табло
        0 – световое табло выключено
        1 – световое табло постоянно включено
        2 – световое табло периодически включается и выключается"""
        if 0 <= mode <= 2:
            self.master.execute(self.__slave, Command.PRESENT_SINGLE_REGISTER, 21, output_value=mode)
        else:
            logging.debug("mode must be between 0 and 2")
