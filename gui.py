import os

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, \
    QHBoxLayout, QComboBox, QPushButton, QColorDialog, QRadioButton, QSlider, \
    QGridLayout, QLabel, QSystemTrayIcon, QAction, QMenu, qApp
from PyQt5.QtGui import QColor, QPalette, QIcon
from PyQt5.QtCore import Qt

from command import Command
from i18n import _

class MainWindow(QMainWindow):
    colorWidget = None
    mode_steady = None
    mode_blink = None
    mode_pulse = None
    speed = None
    notifier = None
    mode = Command.Mode.Steady
    prev_mode = Command.Mode.Blink
    blink_min = 0;
    blink_max = 3000;
    pulse_min = 0;
    pulse_max = 3000;

    def __init__(self, notifier, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.setWindowTitle(_("Status Light Controller"))
        self.setWindowIcon(QIcon('horizontal-traffic-light.ico'))
        self.notifier = notifier

        layout = QGridLayout()

        # Color Picker section
        self.colorWidget = Color('black')
        self.colorWidget.setMouseReleased(self.change_color)
        layout.addWidget(self.colorWidget, 0, 0, 1, 2)

        # status_set = QPushButton(_("Set Status"))
        # status_set.clicked.connect(self.set_status)
        # layout.addWidget(status_set, 0, 1, 1, 2)

        # Mode section
        mode_layout = QVBoxLayout()

        self.mode_steady = QRadioButton(_("Steady"))
        self.mode_steady.setChecked(True)
        self.mode_steady.toggled.connect(lambda: self.change_mode(Command.Mode.Steady))
        mode_layout.addWidget(self.mode_steady)

        self.mode_blink = QRadioButton(_("Blink"))
        self.mode_blink.toggled.connect(lambda: self.change_mode(Command.Mode.Blink))
        mode_layout.addWidget(self.mode_blink)

        self.mode_pulse = QRadioButton(_("Pulse"))
        self.mode_pulse.toggled.connect(lambda: self.change_mode(Command.Mode.Pulse))
        mode_layout.addWidget(self.mode_pulse)

        layout.addLayout(mode_layout, 0, 2, 1, 2)

        # Speed section
        speed_label = QLabel(_("Speed:"))
        layout.addWidget(speed_label, 1, 0, 1, 1)

        self.speed = QSlider(Qt.Horizontal)
        self.speed.setTickPosition(QSlider.TicksBothSides)
        self.speed.setTickInterval(100)
        self.speed.setSingleStep(10)
        self.speed.setMinimum(self.blink_min)
        self.speed.setMaximum(self.blink_max)
        self.speed.setValue((self.blink_max - self.blink_min) / 2)
        self.speed.setEnabled(False)
        self.speed.valueChanged[int].connect(self.change_speed)
        layout.addWidget(self.speed, 1, 1, 1, 3)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        # System Tray Icon
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon('horizontal-traffic-light.ico'))

        show_action = QAction('Show', self)
        quit_action = QAction('Exit', self)
        hide_action = QAction('Hide', self)
        show_action.triggered.connect(self.show)
        hide_action.triggered.connect(self.hide)
        quit_action.triggered.connect(self.close_app)
        tray_menu = QMenu()
        tray_menu.addAction(show_action)
        tray_menu.addAction(hide_action)
        tray_menu.addAction(quit_action)
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

    def change_color(self):
        color = QColorDialog.getColor()
        self.colorWidget.setColor(color)
        self.notifier.set_rgb(
            "{:02x}".format(color.red()),
            "{:02x}".format(color.green()),
            "{:02x}".format(color.blue()))

    def change_mode(self, mode):
        self.notifier.set_mode(mode)
        if mode == Command.Mode.Steady:
            self.speed.setEnabled(False)
        else:
            if self.prev_mode != mode:
                self.convert_range(self.prev_mode, mode)
                self.prev_mode = mode
            self.speed.setEnabled(True)
            self.change_speed()
        self.mode = mode

    def convert_range(self, old_mode, new_mode):
        if old_mode == Command.Mode.Blink:
            old_min = self.blink_min
            old_max = self.blink_max
        elif old_mode == Command.Mode.Pulse:
            old_min = self.pulse_min
            old_max = self.pulse_max

        if new_mode == Command.Mode.Blink:
            new_min = self.blink_min
            new_max = self.blink_max
        elif new_mode == Command.Mode.Pulse:
            new_min = self.pulse_min
            new_max = self.pulse_max

        old_val = self.speed.value()
        old_range = old_max - old_min
        new_range = new_max - new_min
        new_val = (((old_val - old_min) * new_range) / old_range) + new_min
        self.speed.setMinimum(new_min)
        self.speed.setMaximum(new_max)
        self.speed.setValue(new_val)

    def change_speed(self):
        val = self.speed.value()
        speed = (self.speed.maximum() + 1) - val
        self.notifier.set_speed(speed)

    def closeEvent(self, event):
        event.ignore()
        self.hide()
        self.tray_icon.showMessage(
            'Status Light Controller',
            'Application was minimized to tray',
            QSystemTrayIcon.Information,
            2000
        )
        

    def close_app(self, event):
        self.notifier.set_rgb('00', '00', '00')
        qApp.quit()


class Color(QWidget):

    def __init__(self, color, *args, **kwargs):
        super(Color, self).__init__(*args, **kwargs)
        self.setAutoFillBackground(True)
        self.setColor(color)

    def setColor(self, color):
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(color))
        self.setPalette(palette)

    def getColor(self):
        return self.palette().color(QPalette.Window)

    def setMouseReleased(self, callback):
        self.mouseReleaseCallback = callback

    def mouseReleaseEvent(self, event):
        self.mouseReleaseCallback()
