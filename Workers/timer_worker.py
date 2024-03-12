import numpy as np
from PyQt5.QtCore import pyqtSignal, QThread, QTimer
import logging

from Workers.worker import WorkerPattern


class Worker(WorkerPattern):
    def __init__(self, my_thread: QThread | None, memory, parent=None):
        super().__init__(my_thread, parent)
        self.__timer = QTimer()
        self.__timer.start(1000)

    def connect(self, func):
        self.__timer.timeout.connect(func)

    def stop(self):
        logging.debug("TimerWorker() завершил процесс")
        super().stop()
