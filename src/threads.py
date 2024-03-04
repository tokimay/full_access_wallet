from time import sleep
from PyQt6.QtCore import QThread


class Balance(QThread):
    def __init__(self, window):
        super().__init__()
        self.window = window

    def run(self):
        while True:
            sleep(5)
            self.window.getBalance()

