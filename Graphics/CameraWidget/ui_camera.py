from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(418, 323)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setMinimumSize(QtCore.QSize(200, 20))
        self.label_2.setMaximumSize(QtCore.QSize(999999, 20))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_3.addWidget(self.label_2)
        self.lcd_gamma = QtWidgets.QLCDNumber(Form)
        self.lcd_gamma.setMinimumSize(QtCore.QSize(300, 30))
        self.lcd_gamma.setMaximumSize(QtCore.QSize(9999999, 30))
        self.lcd_gamma.setDigitCount(3)
        self.lcd_gamma.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.lcd_gamma.setObjectName("lcd_gamma")
        self.verticalLayout_3.addWidget(self.lcd_gamma)
        self.verticalLayout.addLayout(self.verticalLayout_3)
        self.image_label = QtWidgets.QLabel(Form)
        self.image_label.setMinimumSize(QtCore.QSize(418, 236))
        self.image_label.setAlignment(QtCore.Qt.AlignCenter)
        self.image_label.setObjectName("image_label")
        self.verticalLayout.addWidget(self.image_label)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label_2.setText(_translate("Form", "Сравнение"))
        self.image_label.setText(_translate("Form", "Камера"))
