import cv2
import numpy as np
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtGui import QCursor, QPixmap
from PyQt5 import QtGui

from PyQt5 import QtWidgets

from Graphics.CameraWidget import ui_camera
from Service import convertui
from Workers.memory_keys import Workers

convertui.convertui(__file__, 'ui_camera')


class Widget(QtWidgets.QWidget, ui_camera.Ui_Form):
    def __init__(self, workers_memory, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)
        self.__workers_memory = workers_memory
        self.__image = None
        self.__cursor_x = 0
        self.__cursor_y = 0
        self.__frame_x = 0
        self.__frame_y = 0
        self.__camera_h = 0
        self.__camera_w = 0
        self.__scale_x = 250
        self.__scale_y = 150
        self.__image_label_size = [0, 0]
        self.__cursor_scale = 0

        self.__workers_memory[Workers.camera_worker].change_pixmap_signal.connect(self.update_image)
        self.__workers_memory[Workers.frames_move_worker].connect(self.moveFrame)
        self.__workers_memory[Workers.compare_colors_worker].connect(self.compareColors, 100)

    def mousePressEvent(self, event) -> None:
        if event.button() == Qt.LeftButton:
            self.__cursor_x, self.__cursor_y = self.getCursorPos()
            if self.cursorInFrame():
                self.__workers_memory[Workers.frames_move_worker].startTimer(10)
            event.accept()

    def mouseReleaseEvent(self, event) -> None:
        if event.button() == Qt.LeftButton:
            self.__workers_memory[Workers.frames_move_worker].stopTimer()
            event.accept()

    def wheelEvent(self, event) -> None:
        self.__cursor_x, self.__cursor_y = self.getCursorPos()
        if self.cursorInFrame():
            event.angleDelta()
            angle = event.angleDelta().y()
            if angle > 0:
                if not self.__scale_x < 50:
                    self.__scale_x -= angle
            elif angle < 0:
                if (self.__frame_x + self.__scale_x - angle < self.__camera_w and
                        self.__frame_y + self.__scale_y - angle < self.__camera_h):
                    self.__scale_x -= angle
        event.accept()

    def cursorInFrame(self) -> bool:
        return (self.__frame_x < self.__cursor_x < (self.__frame_x + self.__scale_x)
                and self.__frame_y < self.__cursor_y < (self.__frame_y + self.__scale_y))

    def getCursorPos(self) -> [int, int]:
        cursor_pos = self.image_label.mapFromGlobal(QCursor.pos())
        cursor_x = int((cursor_pos.x() - (self.image_label.width() - self.__image_label_size[0]) // 2) * self.__cursor_scale)
        cursor_y = int((cursor_pos.y() - (self.image_label.height() - self.__image_label_size[1]) // 2) * self.__cursor_scale)
        return cursor_x, cursor_y

    def moveFrame(self) -> None:
        current_cursor_pos_x, current_cursor_pos_y = self.getCursorPos()
        new_x = self.__frame_x + (current_cursor_pos_x - self.__cursor_x)
        new_y = self.__frame_y + (current_cursor_pos_y - self.__cursor_y)
        if new_x >= 0 and (new_x + self.__scale_x) <= self.__camera_w:
            self.__frame_x = new_x
        if new_y >= 0 and (new_y + self.__scale_y) <= self.__camera_h:
            self.__frame_y = new_y
        self.__cursor_x = current_cursor_pos_x
        self.__cursor_y = current_cursor_pos_y

    @pyqtSlot(np.ndarray)
    def update_image(self, cv_img) -> None:
        h, w, ch = cv_img.shape
        self.__image = cv_img
        self.__camera_h = h
        self.__camera_w = w
        self.__scale_y = int(self.__scale_x * (h / w))
        cv2.rectangle(cv_img, (self.__frame_x, self.__frame_y),
                      (self.__frame_x + self.__scale_x, self.__frame_y + self.__scale_y), color=(255, 0, 0), thickness=2)
        cv2.rectangle(cv_img, (w - self.__frame_x - self.__scale_x, self.__frame_y),
                      (w - self.__frame_x, self.__frame_y + self.__scale_y), color=(0, 0, 255), thickness=2)
        qt_img = self.convert_cv_qt(cv_img, h, w, ch)
        self.__image_label_size = [qt_img.width(), qt_img.height()]
        self.__cursor_scale = w / qt_img.width()
        self.image_label.setPixmap(qt_img)

    def convert_cv_qt(self, cv_img, h, w, ch) -> np.ndarray:
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(self.image_label.width(), self.image_label.height(), Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)

    def compareColors(self):
        if self.__image is not None:
            blue_rect_avg = np.mean(
                self.__image[self.__frame_y:self.__frame_y + self.__scale_y, self.__frame_x:self.__frame_x + self.__scale_x],
                axis=(0, 1))
            red_rect_avg = np.mean(
                self.__image[self.__frame_y:self.__frame_y + self.__scale_y, self.__camera_w - self.__frame_x - self.__scale_x:self.__camera_w - self.__frame_x],
                axis=(0, 1))
            self.lcd_gamma.display(int(sum(abs(blue_rect_avg - red_rect_avg))))
