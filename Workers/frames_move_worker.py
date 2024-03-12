import logging

from PyQt5.QtCore import QThread, QTimer

from Workers.worker import WorkerPattern


class Worker(WorkerPattern):
    def __init__(self, my_thread: QThread | None, memory, parent=None):
        super().__init__(my_thread, parent)
        self.__timer = QTimer()

    def connect(self, func):
        self.__timer.timeout.connect(func)

    def startTimer(self, ms):
        self.__timer.start(ms)

    def stopTimer(self):
        self.__timer.stop()

    def stop(self):
        logging.debug("FramesMoveWorker() завершил процесс")
        super().stop()
