import sys

from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QApplication

from Workers import CameraWorker, FramesMoveWorker, TimerWorker, CompareColorsWorker, AmperageSensorsWorker
from Workers.memory_keys import Workers
from Graphics import MainWidget


if __name__ == "__main__":
    application = QApplication(sys.argv)
    workers_memory = {}
    threads_memory = {thread: QThread() for thread in Workers}

    # инициализация воркеров
    workers_memory[Workers.camera_worker] = CameraWorker(threads_memory[Workers.camera_worker], workers_memory)
    workers_memory[Workers.frames_move_worker] = FramesMoveWorker(threads_memory[Workers.frames_move_worker], workers_memory)
    workers_memory[Workers.timer_worker] = TimerWorker(threads_memory[Workers.timer_worker], workers_memory)
    workers_memory[Workers.compare_colors_worker] = CompareColorsWorker(threads_memory[Workers.compare_colors_worker], workers_memory)
    workers_memory[Workers.amperage_sensors_worker] = AmperageSensorsWorker(threads_memory[Workers.amperage_sensors_worker], workers_memory)

    # запуск потоков
    for thread in threads_memory.values():
        thread: QThread()
        thread.start()

    widget = MainWidget(workers_memory, threads_memory)
    widget.show()
    application.exec()

    sys.exit()
