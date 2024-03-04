import sys
from PyQt5.QtWidgets import QApplication
from Graphics import mainWidget

application = QApplication(sys.argv)
widget = mainWidget.Widget()
widget.show()
with open("Graphics/styles.css", "r") as file:
    application.setStyleSheet(file.read())
application.exec()
sys.exit()
