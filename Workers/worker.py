from PyQt5.QtCore import Qt, pyqtSignal, QThread, QObject, QTimer, pyqtSlot
import time
import colorama


class WorkerPattern(QObject):
    """Полноценный шаблон для написания воркеров потоков приложения"""
    stopped_signal = pyqtSignal()  # Сигнал о том, что поток успешно остановлен

    def __init__(self, my_thread: QThread | None, run_period: float = None, parent=None, debugging=False, debug_name=''):
        """my_thread - поток, в который нужно переместить воркера. По умолчанию будет находиться в том же потоке, что и создан. Если передать None - не будет перемещаться никуда
        run_period - период, с которым будет вызываться функция run в секундах
        max_congestion_time - максимально допустимая разность между временем, в которое отправлен сигнал и временем его принятия.
        Если задержка больше - итерации начнут пропускаться"""
        super().__init__(parent)

        self.my_thread = my_thread
        if my_thread is not None:
            self.moveToThread(my_thread)

        self.__debug_name = debug_name
        self.__debugging = debugging

        self.__target_run_period = run_period  # Целевой период вызова функции run. Насколько часто (с каким периодом в секундах) хочет пользователь чтобы запускалась функция
        self.__current_run_period = run_period  # Реальный период, с которым выполняется функция. Рассчитывается динамически

        self.__sum_run_time = 0
        self.__count_run_time = 0
        self.__last_count_time_time = 0

        self.__init_timer = QTimer()
        self.__init_timer.singleShot(0, self.init_in_thread)

        self.__while_timer = None
        self.__IS_RUNNING = False  # Специальная переменная для блокирующих потоков или иногда блокирующих потоков. Блокировка потока обязана сниматься этой переменной

    def init_in_thread(self):

        if self.__target_run_period is not None:
            self.__while_timer = QTimer()
            self.__while_timer.timeout.connect(self.__flow_control)
            self.__while_timer.start(int(self.__target_run_period * 1000))

    @pyqtSlot()
    def __flow_control(self):
        time_start = time.time()

        self.run()
        run_time = time.time() - time_start

        self.__sum_run_time += run_time
        self.__count_run_time += 1

        if time.time() - self.__last_count_time_time >= 1:
            average_time = self.__sum_run_time / self.__count_run_time

            self.__sum_run_time = 0
            self.__count_run_time = 0
            self.__last_count_time_time = time.time()

            if average_time > self.__current_run_period:
                # Замедление цикла. Что-то пошло не по плану
                self.__current_run_period = average_time * 1.1

                delay_new = int(average_time * 1.1 * 1000)
                self.__while_timer.setInterval(delay_new)

                if average_time == 0:
                    print(colorama.Fore.RED,
                          f'НОВАЯ ЗАДЕРЖКА {"ПОТОКА" if not self.__debug_name else self.__debug_name}',
                          round(self.__current_run_period, 4), 'ЗАДАНА: ', self.__target_run_period,
                          'СРЕДНЕЕ ВРЕМЯ РАБОТЫ:', round(average_time, 4), colorama.Fore.RESET)
                else:
                    print(colorama.Fore.RED,
                          f'НОВАЯ ЗАДЕРЖКА {"ПОТОКА" if not self.__debug_name else self.__debug_name}',
                          round(self.__current_run_period, 4), 'ЗАДАНА: ', self.__target_run_period,
                          'СРЕДНЕЕ ВРЕМЯ РАБОТЫ:', round(average_time, 4), 'ЧАСТОТА:', round(1 / average_time, 1),
                          colorama.Fore.RESET)

            elif average_time < self.__current_run_period * 0.7 and self.__current_run_period > self.__target_run_period:
                # Ускорение цикла потому что можно ускоряться, итерация начала выполняться быстро
                self.__current_run_period *= 0.7

                self.__current_run_period = max(self.__target_run_period, self.__current_run_period)

                self.__while_timer.setInterval(int(self.__current_run_period * 1000))

                if self.__current_run_period == self.__target_run_period:
                    print(colorama.Fore.GREEN, f'ПОТОК {"" if not self.__debug_name else self.__debug_name}',
                          f'НОРМОЛИЗОВАЛСЯ (период {self.__current_run_period})', colorama.Fore.RESET)

                elif average_time == 0:
                    print(colorama.Fore.GREEN,
                          f'НОВАЯ ЗАДЕРЖКА {"ПОТОКА" if not self.__debug_name else self.__debug_name}',
                          round(self.__current_run_period, 4), 'ЗАДАНА: ', self.__target_run_period,
                          'СРЕДНЕЕ ВРЕМЯ РАБОТЫ:', round(average_time, 4), colorama.Fore.RESET)

                else:
                    print(colorama.Fore.GREEN,
                          f'НОВАЯ ЗАДЕРЖКА {"ПОТОКА" if not self.__debug_name else self.__debug_name}',
                          round(self.__current_run_period, 4), 'ЗАДАНА: ', self.__target_run_period,
                          'СРЕДНЕЕ ВРЕМЯ РАБОТЫ:', round(average_time, 4), 'ЧАСТОТА:', round(1 / average_time, 1),
                          colorama.Fore.RESET)

            elif self.__debugging:
                if average_time == 0:
                    print(f'Среднее время работы {self.__debug_name}', round(average_time, 4))
                else:
                    print(f'Среднее время работы {self.__debug_name}', round(average_time, 4), 'частота',
                          round(1 / average_time, 2))

    @pyqtSlot()
    def stop(self):
        """ Базовая остановка воркер """
        if self.__while_timer is not None:
            self.__while_timer.stop()
        self.stopped_signal.emit()

    def run(self):
        """ Эту функцию нужно переопределить для того, чтобы написать тело цикла своего потока.
        Функция будет вызываться регулярно раз в заданный при инициализации промежуток времени.
        Ключевое преимущество заключается в том, что в случае, если функция станет занимать слишком
        много времени и очередь QT начнёт копиться, то сигналы начнут пропускаться для очищения очереди.
        В конечном итоге, функция run будет вызываться реже и будет печать в консоль """
        pass
