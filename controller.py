"""
    Status Light Controllers
"""
import sys

from PyQt5.QtWidgets import QApplication

from command import Command
from i18n import _
from gui import MainWindow
from notifier import Notifier


class StatusLight(object):
    """
        Status Light Controller application
    """

    def __init__(self):
        # Setup Notifier connection
        notifier = Notifier()
        addr, name = notifier.discover(2)
        notifier.connect(addr)
        notifier.set_mode(Command.Mode.Steady)

        # Setup GUI
        app = QApplication(sys.argv)
        window = MainWindow(notifier)
        window.show()
        app.exec_()

if __name__ == '__main__':
    StatusLight()
