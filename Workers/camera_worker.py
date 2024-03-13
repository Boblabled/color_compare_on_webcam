import logging

import numpy as np
from PyQt5.QtCore import pyqtSignal, QThread, QTimer

from Workers.worker import WorkerPattern
import cv2


# TODO может вылететь ошибка при закрытии приложения
# TODO сделать проверку на наличие камеры
class Worker(WorkerPattern):
    change_pixmap_signal = pyqtSignal(np.ndarray)

    def __init__(self, my_thread: QThread | None, memory, parent=None):
        super().__init__(my_thread, parent)
        self.__cap = cv2.VideoCapture(0)
        self.__timer = QTimer()
        self.__timer.singleShot(0, self.read)
        self.__IS_RUNNING = True

    # def connect(self, func):
    #     __change_pixmap_signal.connect(func)

    def read(self):
        while self.__IS_RUNNING:
            ret, cv_img = self.__cap.read()
            if ret:
                self.change_pixmap_signal.emit(cv_img)

    def stop(self):
        logging.debug("CameraWorker() завершил процесс")
        self.__IS_RUNNING = False
        # self.cap.release()
        super().stop()
