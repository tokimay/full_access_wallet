from PyQt6 import QtWidgets, uic
from src.gui_mouseTracker import MouseTracker


class Ui(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('UI/CreateNewAccount.ui', self)
        self.setClickEvents()
        self.entropy = ''

    def setClickEvents(self):
        ptn_create_account = self.findChild(QtWidgets.QPushButton, 'pushButton_create_account')
        ptn_create_account.clicked.connect(self.createAccount)
        ptn_create_account = self.findChild(QtWidgets.QPushButton, 'pushButton_cancel')
        ptn_create_account.clicked.connect(self.cancel)

    def createAccount(self):
        self.close()
        childWindow = MouseTracker()
        childWindow.exec()
        self.entropy = childWindow.getEntropy()

    def cancel(self):
        self.entropy = None
        self.close()

    def getRandomEntropy(self):
        return self.entropy




