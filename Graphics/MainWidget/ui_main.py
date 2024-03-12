from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_WidgetName(object):
    def setupUi(self, WidgetName):
        WidgetName.setObjectName("WidgetName")
        WidgetName.resize(836, 769)
        WidgetName.setStyleSheet("")
        self.verticalLayout = QtWidgets.QVBoxLayout(WidgetName)
        self.verticalLayout.setContentsMargins(10, 10, 10, 10)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(WidgetName)
        QtCore.QMetaObject.connectSlotsByName(WidgetName)

    def retranslateUi(self, WidgetName):
        _translate = QtCore.QCoreApplication.translate
        WidgetName.setWindowTitle(_translate("WidgetName", "Виджет"))
