import logging

from PyQt5.QtCore import QThread, QTimer
from Workers.worker import WorkerPattern


class Worker(WorkerPattern):
    def __init__(self, my_thread: QThread | None, memory, parent=None):
        super().__init__(my_thread, parent)
        self.__timer = QTimer()

    def connect(self, func, ms):
        self.__timer.timeout.connect(func)
        self.__timer.start(ms)

    def stop(self):
        logging.debug("CompareColorsWorker() завершил процесс")
        super().stop()
