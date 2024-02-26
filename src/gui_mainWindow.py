import webbrowser
import pyperclip
import web3

import src.account as account
from src import database, types, gui_errorDialog
from PyQt6 import QtWidgets, uic
from PyQt6.QtCore import QSize
from PyQt6.QtGui import QIcon, QPixmap, QAction


class Ui(QtWidgets.QMainWindow):
    def __init__(self, dbName):
        super().__init__()
        uic.loadUi('resources/UI/MainWindow.ui', self)

        self.lineEdit_node_provider = self.findChild(QtWidgets.QLineEdit, 'lineEdit_node_provider')
        self.comboBox_activeAddress_val = self.findChild(QtWidgets.QComboBox, 'comboBox_activeAddress_val')
        self.label_amount_val = self.findChild(QtWidgets.QLabel, 'label_amount_val')
        self.pushButton_copy_address = self.findChild(QtWidgets.QPushButton, 'pushButton_copy_address')
        self.pushButton_ETH = self.findChild(QtWidgets.QPushButton, 'pushButton_ETH')
        self.pushButton_node_provider = self.findChild(QtWidgets.QPushButton, 'pushButton_node_provider')
        self.textEdit_main = self.findChild(QtWidgets.QTextEdit, 'textEdit_main')

        self.actionNew_account = self.findChild(QAction, 'actionNew_account')

        self.actionEntropy = self.findChild(QAction, 'actionEntropy')
        self.actionPrivateKey = self.findChild(QAction, 'actionPrivateKey')
        self.actionPublicKey_coordinates = self.findChild(QAction, 'actionPublicKey_coordinates')
        self.actionPublicKey = self.findChild(QAction, 'actionPublicKey')

        self.db = database.Sqlite(dbName)
        self.initIcons()
        self.setClickEvents()
        self.setMenuActions()
        self.comboBox_activeAddress_val.clear()

    def setClickEvents(self):
        self.pushButton_copy_address.clicked.connect(self.copyAddress)
        self.pushButton_ETH.clicked.connect(self.goToEtherscan)
        self.pushButton_node_provider.clicked.connect(self.goToEtherNodes)
        self.actionNew_account.triggered.connect(self.createAccount)
        self.actionEntropy.triggered.connect(lambda: self.showSecrets(types.SECRET.ENTROPY))
        self.actionPrivateKey.triggered.connect(lambda: self.showSecrets(types.SECRET.PRIVATE_KEY))
        self.actionPublicKey_coordinates.triggered.connect(lambda: self.showSecrets(types.SECRET.PUBLIC_KEY_X))
        self.actionPublicKey.triggered.connect(lambda: self.showSecrets(types.SECRET.PUBLIC_KEY))

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
        if self.db.isAccountExist():
            message = "Some account(s) already exist"
        else:
            message = "There is no account"

        address = account.createAccount(self.db, message)
        if address != 'None':
            self.comboBox_activeAddress_val.addItem(address)
            self.comboBox_activeAddress_val.setCurrentIndex(self.comboBox_activeAddress_val.count() - 1)

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

    def showSecrets(self, secretType: types.SECRET):
        self.textEdit_main.clear()
        if secretType == types.SECRET.PUBLIC_KEY_X or secretType == types.SECRET.PUBLIC_KEY_Y:
            result_X = (self.db.readColumnByCondition(
                columnName=types.SECRET.PUBLIC_KEY_X, condition=self.comboBox_activeAddress_val.currentText()))
            result_Y = (self.db.readColumnByCondition(
                columnName=types.SECRET.PUBLIC_KEY_Y, condition=self.comboBox_activeAddress_val.currentText()))
            print(result_X)
            print(result_Y)
            if (len(result_X) <= 0) or (len(result_Y) <= 0):
                err = gui_errorDialog.Error('Reading database failed')
                err.exec()
            elif (len(result_X) == 1) or (len(result_Y) == 1):
                self.textEdit_main.append(f'Your account PUBLIC_KEY COORDINATE keep it safe:\n')
                self.textEdit_main.append('X : ' + result_X[0][0])
                self.textEdit_main.append('Y : ' + result_Y[0][0])
            else:
                for res in result_X:
                    self.textEdit_main.append('X:' + res[0][0])
                for res in result_Y:
                    self.textEdit_main.append('Y:' + res[0][0])
        else:
            result = (self.db.readColumnByCondition(
                columnName=secretType, condition=self.comboBox_activeAddress_val.currentText()))
            if len(result) <= 0:
                err = gui_errorDialog.Error('Reading database failed')
                err.exec()
            elif len(result) == 1:
                self.textEdit_main.append(f'Your account {secretType.name} keep it safe:\n')
                self.textEdit_main.append(result[0][0])
            else:
                for res in result:
                    self.textEdit_main.append(res[0])

