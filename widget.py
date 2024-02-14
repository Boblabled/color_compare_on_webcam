import cv2

import convertui
import ui_pyqt
import numpy as np
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot, Qt, QTimer
from PyQt5.QtGui import QPixmap, QCursor

# convertui.convertui(__file__, 'ui_pyqt')


class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)

    def __init__(self):
        super().__init__()
        self._run_flag = True

    def run(self):
        cap = cv2.VideoCapture(0)
        while self._run_flag:
            ret, cv_img = cap.read()
            if ret:
                self.change_pixmap_signal.emit(cv_img)
        cap.release()

    def stop(self):
        self._run_flag = False
        self.wait()


class Widget(QtWidgets.QWidget, ui_pyqt.Ui_WidgetName):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)
        self.image = None
        self.image_label_size = [0, 0]
        self.camera_h = 0
        self.camera_w = 0
        self.timer_flag = False
        self.time = 0
        self.frame_x = 0
        self.frame_y = 0
        self.scale_x = 200
        self.scale_y = 150
        self.cursor_x = 0
        self.cursor_y = 0
        self.cursor_scale = 0

        self.video_thread = VideoThread()
        self.video_thread.change_pixmap_signal.connect(self.update_image)
        self.video_thread.start()

        timer = QTimer(self)
        timer.timeout.connect(self.showTime)
        timer.start(1000)

        self.start_button.pressed.connect(self.start)
        self.stop_button.pressed.connect(self.stop)
        self.reset_button.pressed.connect(self.reset)

        compare_timer = QTimer(self)
        compare_timer.timeout.connect(self.compareColors)
        compare_timer.start(1000)

        self.frame_move_timer = QTimer(self)
        self.frame_move_timer.timeout.connect(self.moveFrame)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.cursor_x, self.cursor_y = self.getCursorPos()
            if self.cursorInFrame():
                self.frame_move_timer.start(10)
            event.accept()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.frame_move_timer.stop()
            event.accept()

    def wheelEvent(self, event):
        self.cursor_x, self.cursor_y = self.getCursorPos()
        if self.cursorInFrame():
            event.angleDelta()
            angle = event.angleDelta().y()
            if angle > 0:
                if not self.scale_x < 50:
                    self.scale_x -= angle
            elif angle < 0:
                if (self.frame_x + self.scale_x - angle < self.camera_w and
                        self.frame_y + self.scale_y - angle < self.camera_h):
                    self.scale_x -= angle
        event.accept()

    def cursorInFrame(self):
        return (self.frame_x < self.cursor_x < (self.frame_x + self.scale_x)
                and self.frame_y < self.cursor_y < (self.frame_y + self.scale_y))

    def getCursorPos(self):
        cursor_pos = self.image_label.mapFromGlobal(QCursor.pos())
        cursor_x = int((cursor_pos.x() - (self.image_label.width() - self.image_label_size[0])//2) * self.cursor_scale)
        cursor_y = int((cursor_pos.y() - (self.image_label.height() - self.image_label_size[1])//2) * self.cursor_scale)
        return cursor_x, cursor_y

    def moveFrame(self):
        current_cursor_pos_x, current_cursor_pos_y = self.getCursorPos()
        new_x = self.frame_x + (current_cursor_pos_x - self.cursor_x)
        new_y = self.frame_y + (current_cursor_pos_y - self.cursor_y)
        if new_x >= 0 and (new_x + self.scale_x) <= self.camera_w:
            self.frame_x = new_x
        if new_y >= 0 and (new_y + self.scale_y) <= self.camera_h:
            self.frame_y = new_y
        self.cursor_x = current_cursor_pos_x
        self.cursor_y = current_cursor_pos_y

    @pyqtSlot(np.ndarray)
    def update_image(self, cv_img):
        h, w, ch = cv_img.shape
        self.image = cv_img
        self.camera_h = h
        self.camera_w = w
        self.scale_y = int(self.scale_x * (h / w))
        cv2.rectangle(cv_img, (self.frame_x, self.frame_y),
                      (self.frame_x + self.scale_x, self.frame_y + self.scale_y), color=(255, 0, 0), thickness=2)
        cv2.rectangle(cv_img, (w - self.frame_x - self.scale_x, self.frame_y),
                      (w - self.frame_x, self.frame_y + self.scale_y), color=(0, 0, 255), thickness=2)
        qt_img = self.convert_cv_qt(cv_img, h, w, ch)
        self.image_label.setPixmap(qt_img)

    def convert_cv_qt(self, cv_img, h, w, ch):
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(self.image_label.width(), self.image_label.height(), Qt.KeepAspectRatio)
        self.cursor_scale = w / p.width()
        self.image_label_size = [p.width(), p.height()]
        return QPixmap.fromImage(p)

    def compareColors(self):
        if self.image is not None:
            blue_rect_avg = np.mean(
                self.image[self.frame_y:self.frame_y + self.scale_y, self.frame_x:self.frame_x + self.scale_x],
                axis=(0, 1))
            red_rect_avg = np.mean(
                self.image[self.frame_y:self.frame_y + self.scale_y, self.camera_w - self.frame_x - self.scale_x:self.camera_w - self.frame_x],
                axis=(0, 1))
            self.lcd_gamma.display(int(sum(abs(blue_rect_avg - red_rect_avg))))

    def showTime(self):
        if self.timer_flag:
            self.time += 1
        self.lcd_timer.display("%02d:%02d:%02d" % (self.time // 1200, self.time % 1200 // 60, self.time % 60))

    def start(self):
        self.timer_flag = True

    def stop(self):
        self.timer_flag = False

    def reset(self):
        self.timer_flag = False
        self.time = 0
        self.lcd_timer.display("00:00:00")

    def closeEvent(self, event):
        self.video_thread.stop()
        event.accept()
