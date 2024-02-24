import webbrowser
from time import sleep

import pyperclip
import src.account as account
from src import database, gui_errorDialog
from PyQt6 import QtWidgets, uic
from PyQt6.QtCore import QSize
from PyQt6.QtGui import QIcon, QPixmap, QAction
import web3


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('UI/MainWindow.ui', self)

        self.lineEdit_node_provider = self.findChild(QtWidgets.QLineEdit, 'lineEdit_node_provider')
        self.comboBox_activeAddress_val = self.findChild(QtWidgets.QComboBox, 'comboBox_activeAddress_val')
        self.label_amount_val = self.findChild(QtWidgets.QLabel, 'label_amount_val')
        self.pushButton_copy_address = self.findChild(QtWidgets.QPushButton, 'pushButton_copy_address')
        self.pushButton_ETH = self.findChild(QtWidgets.QPushButton, 'pushButton_ETH')
        self.pushButton_node_provider = self.findChild(QtWidgets.QPushButton, 'pushButton_node_provider')

        self.initIcons()
        self.setClickEvents()
        self.setMenuActions()

        self.findChild(QtWidgets.QComboBox, 'comboBox_activeAddress_val').clear()

    def setClickEvents(self):
        self.pushButton_copy_address.clicked.connect(self.copyAddress)
        self.pushButton_ETH.clicked.connect(self.goToEtherscan)
        self.pushButton_node_provider.clicked.connect(self.goToEtherNodes)

    def initIcons(self):
        icon = QIcon()

        icon.addPixmap(QPixmap('UI/icons/copy_w.png'))
        self.pushButton_copy_address.setIcon(icon)
        self.pushButton_copy_address.setIconSize(QSize(16, 16))

        icon.addPixmap(QPixmap('UI/icons/ethereum_c_b.png'))
        self.pushButton_ETH.setIcon(icon)
        self.pushButton_ETH.setIconSize(QSize(16, 16))

        icon.addPixmap(QPixmap('UI/icons/ethereum_node_clr.png'))
        self.pushButton_node_provider.setIcon(icon)
        self.pushButton_node_provider.setIconSize(QSize(16, 16))

    def setMenuActions(self):
        actionNew_account = self.findChild(QAction, 'actionNew_account')
        actionNew_account.setShortcut('Ctrl+n')
        actionNew_account.setStatusTip('create new account')

    def createAccount(self):
        acc = account.createAccount()
        if isinstance(acc, dict):
            # print('privateKeyHex', hex(acc['privateKey']), type(acc['privateKey']))
            # print('publicKeyCoordinate', acc['publicKeyCoordinate'], type(acc['publicKeyCoordinate']))
            # print('publicKey', hex(acc['publicKey']), type(acc['publicKey']))
            # print('address', hex(acc['address']), type(acc['address']))
            self.comboBox_activeAddress_val.addItem(hex(acc['address']))
            db = database.Sqlite('Data')
            db.insertRow(acc)
        else:
            err = gui_errorDialog.Error('Account creation failed \n ' + str(type(acc)))
            err.show()

    def goToEtherscan(self):
        active_address = self.comboBox_activeAddress_val.currentText()
        if active_address is not None:
            webbrowser.open('https://etherscan.io/address/' + active_address)

    @staticmethod
    def goToEtherNodes():
        webbrowser.open('https://ethereumnodes.com/')

    def copyAddress(self):
        active_address = self.comboBox_activeAddress_val.currentText()
        if active_address is not None:
            pyperclip.copy(active_address)
        # spam = pyperclip.paste()

    def getBalance(self):
        w3 = web3.Web3(web3.HTTPProvider(self.lineEdit_node_provider.text()))
        address_cksm = web3.Web3.to_checksum_address(self.comboBox_activeAddress_val.currentText())
        balance = w3.eth.get_balance(address_cksm)
        balance = web3.Web3.from_wei(balance, 'ether')
        self.label_amount_val.setText(str(balance))
        print('balance = ', balance)
