from PyQt5 import QtWidgets

from Graphics.ToolsWidget import ui_tools
from Service import convertui

convertui.convertui(__file__, 'ui_tools')


class Widget(QtWidgets.QWidget, ui_tools.Ui_Form):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)

