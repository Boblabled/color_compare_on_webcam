from PyQt5 import QtWidgets
import logging
import colorlog

from Graphics.LoggerWidget import ui_logger
from Service import convertui
from enum import Enum

convertui.convertui(__file__, 'ui_logger')


class Colors(Enum):
    green = "#A4C27C"
    white = "#9EA4B2"
    yellow = "#9D8925"
    red = "#C76B74"


class QTextEditLogger(logging.Handler):
    def __init__(self, parent):
        super().__init__()
        self.widget = QtWidgets.QTextEdit(parent)
        self.widget.setReadOnly(True)

    def emit(self, record):
        msg = self.format(record)
        self.append_text(msg, record.levelname)

    def append_text(self, msg: str, levelName: str):
        new_msg = msg
        tag = '<font color="{}">{}</font>'
        if levelName == 'DEBUG':
            new_msg = tag.format(Colors.green.value, msg)
        elif levelName == 'INFO':
            new_msg = tag.format(Colors.white.value, msg)
        elif levelName == 'WARNING':
            new_msg = tag.format(Colors.yellow.value, msg)
        elif levelName == 'ERROR':
            new_msg = tag.format(Colors.red.value, msg)
        elif levelName == 'CRITICAL':
            new_msg = ("<strong>" + tag + "</strong>").format(Colors.red.value, msg)
        self.widget.append(new_msg)


class Widget(QtWidgets.QWidget, ui_logger.Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setMaximumHeight(200)
        logTextBox = QTextEditLogger(self)
        self.gridLayout.addWidget(logTextBox.widget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)

        # временный костыль
        logging.getLogger().removeHandler(logging.getLogger().handlers[0])

        formatter = "%(asctime)s - %(levelname)s - %(message)s"
        formatter_for_console = colorlog.ColoredFormatter(
            '%(log_color)s' + formatter,
            log_colors={
                'DEBUG': 'green',
                'INFO': 'white',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'bold_red',
            }
        )
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter_for_console)
        logging.getLogger().addHandler(console_handler)

        logTextBox.setFormatter(logging.Formatter(formatter))
        logging.getLogger().addHandler(logTextBox)

        # тест

        for i in range(1):
            logging.debug("Debug message")
            logging.info("Info message")
            logging.warning("Warning message")
            logging.error("Error message")
            logging.critical("Critical message")

