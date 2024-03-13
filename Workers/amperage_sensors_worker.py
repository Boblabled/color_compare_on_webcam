from PyQt5.QtCore import QThread, QTimer
import logging

from Workers.worker import WorkerPattern


class Worker(WorkerPattern):
    def __init__(self, my_thread: QThread | None, memory, parent=None):
        super().__init__(my_thread, parent)
        self.__timer = QTimer()
        self.__ms = 0

    def connect(self, func, ms):
        self.__ms = ms
        self.__timer.timeout.connect(func)

    def pause(self):
        if self.__timer.isActive():
            self.__timer.stop()

    def resume(self):
        if not self.__timer.isActive():
            self.__timer.start(self.__ms)

    def stop(self):
        logging.debug("AmperageSensorsWorker() завершил процесс")
        super().stop()
