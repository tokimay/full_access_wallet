import webbrowser
import pyperclip
import src.account as account
from src import database
from PyQt6 import QtWidgets, uic
from PyQt6.QtCore import QSize
from PyQt6.QtGui import QIcon, QPixmap, QAction


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        # super(Ui, self).__init__()
        uic.loadUi('UI/MainWindow.ui', self)

        self.initIcons()
        self.setClickEvents()
        self.setMenuActions()

        self.findChild(QtWidgets.QComboBox, 'comboBox_activeAddress_val').clear()

    def setClickEvents(self):
        (self.findChild(QtWidgets.QPushButton, 'pushButton_copy_address')
         .clicked.connect(self.copyAddress))
        (self.findChild(QtWidgets.QPushButton, 'pushButton_ETH')
         .clicked.connect(self.goToEtherscan))
        (self.findChild(QtWidgets.QPushButton, 'pushButton_node_provider')
         .clicked.connect(self.goToEtherNodes))

    def initIcons(self):
        self.setIcons(QtWidgets.QPushButton, 'pushButton_copy_address',
                      'UI/icons/copy_w.png')
        self.setIcons(QtWidgets.QPushButton, 'pushButton_ETH',
                      'UI/icons/ethereum_c_b.png')
        self.setIcons(QtWidgets.QPushButton, 'pushButton_node_provider',
                      'UI/icons/ethereum_node_clr.png')

    def setIcons(self, elementType, elementName, iconPath, width=16, height=16):
        icon = QIcon()
        icon.addPixmap(QPixmap(iconPath))
        element = self.findChild(elementType, elementName)
        element.setIcon(icon)
        element.setIconSize(QSize(width, height))

    def setMenuActions(self):
        actionNew_account = self.findChild(QAction, 'actionNew_account')
        actionNew_account.setShortcut('Ctrl+n')
        actionNew_account.setStatusTip('create new account')

    def createAccount(self):
        acc = account.createAccount()
        if isinstance(acc, dict):
            print('privateKeyHex', hex(acc['privateKey']), type(acc['privateKey']))
            print('publicKeyCoordinate', acc['publicKeyCoordinate'], type(acc['publicKeyCoordinate']))
            print('publicKey', hex(acc['publicKey']), type(acc['publicKey']))
            print('address', hex(acc['address']), type(acc['address']))
            self.addTextToCombobox('comboBox_activeAddress_val', hex(acc['address']))
            db = database.sqlite('Data')
            db.insertRow([
                bin(acc['privateKey'])[2:].zfill(256),  # convert hex to 256 bit string binary as entropy
                hex(acc['privateKey']),
                hex(acc['publicKeyCoordinate'][0]),
                hex(acc['publicKeyCoordinate'][1]),
                hex(acc['publicKey']),
                hex(acc['address'])
            ])

    def goToEtherscan(self):
        active_address = self.getComboboxCurrentText('comboBox_activeAddress_val')
        if active_address is not None:
            webbrowser.open('https://etherscan.io/address/' + active_address)

    @staticmethod
    def goToEtherNodes():
        webbrowser.open('https://ethereumnodes.com/')

    def copyAddress(self):
        active_address = self.getComboboxCurrentText('comboBox_activeAddress_val')
        if active_address is not None:
            pyperclip.copy(active_address)
        # spam = pyperclip.paste()

    def changeVisibility(self, elementType, elementName, visibility):
        pass
        # element = self.findChild(elementType, elementName)
        # element.setVisible(visibility)

    def setText(self, elementType, elementName, text):
        self.findChild(elementType, elementName).setText(text)

    def getText(self, elementType, elementName):
        return self.findChild(elementType, elementName).text()

    def addTextToCombobox(self, elementName, text):
        self.findChild(QtWidgets.QComboBox, elementName).addItem(text)

    def getComboboxCurrentText(self, elementName):
        return self.findChild(QtWidgets.QComboBox, elementName).currentText()
