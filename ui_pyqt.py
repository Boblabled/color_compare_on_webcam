from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_WidgetName(object):
    def setupUi(self, WidgetName):
        WidgetName.setObjectName("WidgetName")
        WidgetName.resize(471, 313)
        self.verticalLayout = QtWidgets.QVBoxLayout(WidgetName)
        self.verticalLayout.setObjectName("verticalLayout")
        self.image_label = QtWidgets.QLabel(WidgetName)
        self.image_label.setAlignment(QtCore.Qt.AlignCenter)
        self.image_label.setObjectName("image_label")
        self.verticalLayout.addWidget(self.image_label)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_2 = QtWidgets.QLabel(WidgetName)
        self.label_2.setMaximumSize(QtCore.QSize(16777215, 30))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_3.addWidget(self.label_2)
        self.lcd_gamma = QtWidgets.QLCDNumber(WidgetName)
        self.lcd_gamma.setDigitCount(3)
        self.lcd_gamma.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.lcd_gamma.setObjectName("lcd_gamma")
        self.verticalLayout_3.addWidget(self.lcd_gamma)
        self.label = QtWidgets.QLabel(WidgetName)
        self.label.setMaximumSize(QtCore.QSize(16777215, 30))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout_3.addWidget(self.label)
        self.lcd_timer = QtWidgets.QLCDNumber(WidgetName)
        self.lcd_timer.setMaximumSize(QtCore.QSize(16777215, 150))
        self.lcd_timer.setFrameShape(QtWidgets.QFrame.Box)
        self.lcd_timer.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.lcd_timer.setDigitCount(8)
        self.lcd_timer.setMode(QtWidgets.QLCDNumber.Dec)
        self.lcd_timer.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.lcd_timer.setProperty("value", 0.0)
        self.lcd_timer.setObjectName("lcd_timer")
        self.verticalLayout_3.addWidget(self.lcd_timer)
        self.horizontalLayout.addLayout(self.verticalLayout_3)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.start_button = QtWidgets.QPushButton(WidgetName)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.start_button.sizePolicy().hasHeightForWidth())
        self.start_button.setSizePolicy(sizePolicy)
        self.start_button.setMaximumSize(QtCore.QSize(200, 50))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.start_button.setFont(font)
        self.start_button.setObjectName("start_button")
        self.verticalLayout_2.addWidget(self.start_button)
        self.stop_button = QtWidgets.QPushButton(WidgetName)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.stop_button.sizePolicy().hasHeightForWidth())
        self.stop_button.setSizePolicy(sizePolicy)
        self.stop_button.setMaximumSize(QtCore.QSize(200, 50))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.stop_button.setFont(font)
        self.stop_button.setObjectName("stop_button")
        self.verticalLayout_2.addWidget(self.stop_button)
        self.reset_button = QtWidgets.QPushButton(WidgetName)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.reset_button.sizePolicy().hasHeightForWidth())
        self.reset_button.setSizePolicy(sizePolicy)
        self.reset_button.setMaximumSize(QtCore.QSize(200, 50))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.reset_button.setFont(font)
        self.reset_button.setObjectName("reset_button")
        self.verticalLayout_2.addWidget(self.reset_button)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(WidgetName)
        QtCore.QMetaObject.connectSlotsByName(WidgetName)

    def retranslateUi(self, WidgetName):
        _translate = QtCore.QCoreApplication.translate
        WidgetName.setWindowTitle(_translate("WidgetName", "Виджет"))
        self.image_label.setText(_translate("WidgetName", "Камера"))
        self.label_2.setText(_translate("WidgetName", "Сравнение"))
        self.label.setText(_translate("WidgetName", "Таймер"))
        self.start_button.setText(_translate("WidgetName", "Старт"))
        self.stop_button.setText(_translate("WidgetName", "Стоп"))
        self.reset_button.setText(_translate("WidgetName", "Сброс"))
