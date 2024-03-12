from webbrowser import open as web_browser_open
from pyperclip import copy
from PyQt6.QtWidgets import (QWidget, QGridLayout, QLabel, QPushButton, QComboBox, QLineEdit,
                             QRadioButton, QTextEdit, QMenuBar, QMenu, QStatusBar)
from PyQt6.QtWidgets import QFrame
from json import loads, dump, dumps
from PyQt6 import QtWidgets, QtGui
from PyQt6.QtCore import QSize, QRect
from PyQt6.QtGui import QIcon, QPixmap, QAction, QTextCursor
from src import (database, dataTypes, ethereum,
                 account, system)
from src.GUI import qui_getUserChoice, qui_getUserInput, gui_errorDialog, qui_showMessage
from pathlib import Path
from tkinter import filedialog, Tk

from src.cryptography import DES


class Ui(QtWidgets.QMainWindow):
    def __init__(self, dbName):
        super().__init__()
        self.menubar_file = QMenuBar(self)

        self.menu_wallet = QMenu(self.menubar_file)
        self.menu_newAccount = QMenu(self.menu_wallet)
        self.menu_secrets = QMenu(self.menu_wallet)
        self.menu_backupAndRestore = QMenu(self.menu_wallet)

        self.menu_network = QMenu(self.menubar_file)
        self.menu_transactions = QMenu(self.menu_network)
        self.menu_tools = QMenu(self.menu_network)
        # ----------------------------------------------------------------------------------
        self.action_entropy = QAction(self)
        self.action_privateKey = QAction(self)
        self.action_publicKeyCoordinates = QAction(self)
        self.action_publicKey = QAction(self)
        self.action_mnemonic = QAction(self)
        # ----------------------------------------------------------------------------------
        self.action_newRandomAccount = QAction(self)
        self.action_recoverFromMnemonic = QAction(self)
        self.action_recoverFromEntropy = QAction(self)
        self.action_recoverFromPrivateKey = QAction(self)
        # ----------------------------------------------------------------------------------
        self.action_backup = QAction(self)
        self.action_restore = QAction(self)
        # ----------------------------------------------------------------------------------
        self.action_checkTx = QAction(self)
        self.action_txNonce = QAction(self)
        self.action_simpleHistory = QAction(self)
        self.action_allNormal = QAction(self)
        self.action_allInternal = QAction(self)
        # ----------------------------------------------------------------------------------
        self.action_publicKeyFromTxHash = QAction(self)
        self.action_transactionMessage = QAction(self)
        # ----------------------------------------------------------------------------------
        self.central_widget = QWidget(self)
        self.gridLayout_widget = QWidget(self.central_widget)
        self.gridlayout = QGridLayout(self.gridLayout_widget)
        # ----------------------------------------------------------------------------------
        # row 1
        self.label_nodeProvider = QLabel(self.gridLayout_widget)
        self.lineEdit_nodeProvider = QLineEdit(self.gridLayout_widget)
        self.pushButton_nodeProvider = QPushButton(self.gridLayout_widget)

        # row 2
        self.label_accountName = QLabel(self.gridLayout_widget)
        self.lineEdit_accountName = QLineEdit(self.gridLayout_widget)
        self.pushButton_accountName = QPushButton(self.gridLayout_widget)
        self.pushButton_deleteAccount = QPushButton(self.gridLayout_widget)

        # row 3
        self.label_activeAddress = QLabel(self.gridLayout_widget)
        self.comboBox_activeAddressVal = QComboBox(self.gridLayout_widget)
        self.pushButton_copyAddress = QPushButton(self.gridLayout_widget)

        # row 4
        self.label_amount = QLabel(self.gridLayout_widget)
        self.label_amountVal = QLabel(self.gridLayout_widget)
        self.pushButton_etherScan = QPushButton(self.gridLayout_widget)

        # row 5
        self.label_send = QLabel(self.gridLayout_widget)
        self.lineEdit_send = QLineEdit(self.gridLayout_widget)
        self.pushButton_send = QPushButton(self.gridLayout_widget)

        # row 6
        self.label_sendValue = QLabel(self.gridLayout_widget)
        self.lineEdit_sendValue = QLineEdit(self.gridLayout_widget)
        self.label_message = QLabel(self.gridLayout_widget)
        self.lineEdit_message = QLineEdit(self.gridLayout_widget)

        # row 7
        self.textEdit_main = QTextEdit(self.gridLayout_widget)

        # customization
        self.label_customizationArea = QLabel(self.gridLayout_widget)
        self.radioButton_mainNet = QRadioButton(self.gridLayout_widget)
        self.radioButton_testNet = QRadioButton(self.gridLayout_widget)

        self.line_vertical = QFrame(self.gridLayout_widget)
        # ----------------------------------------------------------------------------------
        self.statusbar = QStatusBar(self)

        self.db = database.Sqlite(dbName)
        self.initUI()
        self.initIcons()
        self.initStyleSheet()
        self.setClickEvents()
        self.setMenuActions()

    def initUI(self):
        self.setObjectName("MainWindow")
        self.setWindowTitle("FAwallet")
        self.resize(800, 600)
        self.setFixedSize(800, 600)
        self.setMenuBar(self.menubar_file)

        self.setCentralWidget(self.central_widget)
        self.central_widget.setObjectName("centralWidget")
        self.gridLayout_widget.setObjectName("gridLayoutWidget")
        self.gridLayout_widget.setGeometry(QRect(10, 10, 780, 580))
        self.gridlayout.setObjectName("gridlayout")
        self.gridlayout.setGeometry(QRect(10, 10, 780, 580))
        self.gridlayout.setContentsMargins(0, 0, 0, 0)
        # ----------------------------------------------------------------------------------
        self.action_entropy.setObjectName("actionEntropy")
        self.action_privateKey.setObjectName("actionPrivateKey")
        self.action_publicKeyCoordinates.setObjectName("actionPublicKey_coordinates")
        self.action_publicKey.setObjectName("actionPublicKey")
        self.action_mnemonic.setObjectName("actionMnemonic")

        self.action_newRandomAccount.setObjectName("actionNewRandomAccount")
        self.action_recoverFromMnemonic.setObjectName("actionRecover_from_mnemonic")
        self.action_recoverFromEntropy.setObjectName("actionRecover_from_entropy")
        self.action_recoverFromPrivateKey.setObjectName("actionRecover_from_privateKey")
        # ----------------------------------------------------------------------------------
        self.action_checkTx.setObjectName("action_checkTX")
        self.action_txNonce.setObjectName("actionTX_nonce")
        self.action_simpleHistory.setObjectName("actionSimple_history")
        self.action_allNormal.setObjectName("actionAll_normal")
        self.action_allInternal.setObjectName("actionAll_internal")

        self.action_publicKeyFromTxHash.setObjectName("actionPublicKey_from_TXHash")
        self.action_transactionMessage.setObjectName('actionTransactionMessage')
        # ----------------------------------------------------------------------------------
        self.menubar_file.setObjectName("menubar_file")
        self.menubar_file.setGeometry(QRect(0, 0, 800, 30))
        # ----------------------------------------------------------------------------------
        # wallet menu
        self.menubar_file.addAction(self.menu_wallet.menuAction())
        self.menu_wallet.setObjectName("menu_Wallet")
        self.menu_wallet.setTitle("&Wallet")

        #  wallet menu -> account menu
        self.menu_wallet.addAction(self.menu_newAccount.menuAction())
        self.menu_newAccount.setObjectName("menuNew_account")
        self.menu_newAccount.setTitle("New account")
        self.menu_newAccount.addAction(self.action_newRandomAccount)
        self.action_newRandomAccount.setText("New random account")
        self.menu_newAccount.addAction(self.action_recoverFromMnemonic)
        self.action_recoverFromMnemonic.setText("Recover from mnemonic")
        self.menu_newAccount.addAction(self.action_recoverFromEntropy)
        self.action_recoverFromEntropy.setText("Recover from entropy")
        self.menu_newAccount.addAction(self.action_recoverFromPrivateKey)
        self.action_recoverFromPrivateKey.setText("Recover from privateKey")

        #  wallet menu -> Secrets menu
        self.menu_wallet.addAction(self.menu_secrets.menuAction())
        self.menu_secrets.setObjectName("menuSecrets")
        self.menu_secrets.setTitle("Secrets")
        # self.menuSecrets.addSeparator()
        self.menu_secrets.addAction(self.action_entropy)
        self.action_entropy.setText("Entropy")
        self.menu_secrets.addAction(self.action_privateKey)
        self.action_privateKey.setText("PrivateKey")
        self.menu_secrets.addAction(self.action_publicKeyCoordinates)
        self.action_publicKeyCoordinates.setText("PublicKey coordinates")
        self.menu_secrets.addAction(self.action_publicKey)
        self.action_publicKey.setText('PublicKey')
        self.menu_secrets.addAction(self.action_mnemonic)
        self.action_mnemonic.setText("Mnemonic")

        #  wallet menu -> Backup and restore menu
        self.menu_wallet.addAction(self.menu_backupAndRestore.menuAction())
        self.menu_backupAndRestore.setObjectName("menuBackupAndRestore")
        self.menu_backupAndRestore.setTitle("Backup and Restore")
        self.menu_backupAndRestore.addAction(self.action_backup)
        self.action_backup.setText("Backup account")
        self.menu_backupAndRestore.addAction(self.action_restore)
        self.action_restore.setText('Restore account')

        # ----------------------------------------------------------------------------------
        # Network menu
        self.menubar_file.addAction(self.menu_network.menuAction())
        self.menu_network.setObjectName("menu_network")
        self.menu_network.setTitle("&Network")

        # Network menu -> Transactions menu
        self.menu_network.addAction(self.menu_transactions.menuAction())
        self.menu_transactions.setObjectName("menu_transactions")
        self.menu_transactions.setTitle("Transactions")
        self.menu_transactions.addAction(self.action_checkTx)
        self.action_checkTx.setText("Check transaction")
        self.menu_transactions.addAction(self.action_txNonce)
        self.action_txNonce.setText("Transaction nounce")
        self.menu_transactions.addAction(self.action_simpleHistory)
        self.action_simpleHistory.setText("Simple history(need APIkey)")
        self.menu_transactions.addAction(self.action_allNormal)
        self.action_allNormal.setText("All normal TXS (need APIkey)")
        self.menu_transactions.addAction(self.action_allInternal)
        self.action_allInternal.setText("All internal TXS (need APIkey)")

        # Network menu -> Tools menu
        self.menu_network.addAction(self.menu_tools.menuAction())
        self.menu_tools.setObjectName("menu_tools")
        self.menu_tools.setTitle("Tools")
        self.menu_tools.addAction(self.action_publicKeyFromTxHash)
        self.action_publicKeyFromTxHash.setText("PublicKey from TXHash")
        self.menu_tools.addAction(self.action_transactionMessage)
        self.action_transactionMessage.setText('Show transaction message')
        # ----------------------------------------------------------------------------------
        # row 1
        self.label_nodeProvider.setObjectName("label_nodeProvider")
        self.label_nodeProvider.setText("Node provider:")
        self.lineEdit_nodeProvider.setText("https://nodes.mewapi.io/rpc/eth")
        self.lineEdit_nodeProvider.setObjectName("lineEdit_nodeProvider")
        self.pushButton_nodeProvider.setObjectName("pushButton_nodeProvider")
        self.pushButton_nodeProvider.setText("Providers")

        # row 2
        self.label_accountName.setObjectName("label_accountName")
        self.label_accountName.setText("Account name:")
        self.lineEdit_accountName.setObjectName("lineEdit_accountName")
        self.pushButton_accountName.setObjectName("pushButton_accountName")
        self.pushButton_accountName.setText("Edit")
        self.pushButton_deleteAccount.setObjectName("pushButton_deleteAccount")
        self.pushButton_deleteAccount.setText('Delete current account')

        # row 3
        self.label_activeAddress.setObjectName("label_activeAddress")
        self.label_activeAddress.setText("Active address:")
        self.comboBox_activeAddressVal.setObjectName("comboBox_activeAddressVal")
        self.pushButton_copyAddress.setObjectName("pushButton_copyAddress")
        self.pushButton_copyAddress.setText("Copy address")

        # row 4
        self.label_amount.setObjectName("label_amount")
        self.label_amount.setText("Amount:")
        self.label_amountVal.setObjectName("label_amountVal")
        self.label_amountVal.setText("0")
        self.pushButton_etherScan.setObjectName("pushButton_etherScan")
        self.pushButton_etherScan.setText("etherescan.io")

        # row 5
        self.label_send.setObjectName("label_send")
        self.label_send.setText("Send ETH to:")
        self.lineEdit_send.setObjectName("lineEdit_send")
        self.pushButton_send.setObjectName("pushButton_send")
        self.pushButton_send.setText("Send TX")

        # row 6
        self.label_sendValue.setObjectName("label_sendValue")
        self.label_sendValue.setText("Value to send:")
        self.lineEdit_sendValue.setObjectName("lineEdit_sendValue")
        self.label_message.setObjectName("label_message")
        self.label_message.setText("Message:")
        self.lineEdit_message.setObjectName("lineEdit_message")

        # row 7
        self.textEdit_main.setObjectName("textEdit_main")

        # customization
        self.label_customizationArea.setObjectName("label_customizationArea")
        self.label_customizationArea.setText("Customization area")
        self.radioButton_mainNet.setObjectName("radioButton_mainNet")
        self.radioButton_mainNet.setText("MainNet")
        self.radioButton_testNet.setObjectName("radioButton_testNet")
        self.radioButton_testNet.setText("TestNet(Sepolia)")

        self.line_vertical.setObjectName("line_vertical")
        self.line_vertical.setFrameShape(QFrame.Shape.VLine)
        # self.line_vertical.setFrameShadow(QFrame.Shape.Sunken)
        # ----------------------------------------------------------------------------------
        self.setStatusBar(self.statusbar)
        self.statusbar.setObjectName("statusbar")
        # ----------------------------------------------------------------------------------
        # row 1
        self.gridlayout.addWidget(self.label_nodeProvider, 1, 0, 1, 1)
        self.gridlayout.addWidget(self.lineEdit_nodeProvider, 1, 1, 1, 3)
        self.gridlayout.addWidget(self.pushButton_nodeProvider, 1, 4, 1, 1)
        self.gridlayout.addWidget(self.line_vertical, 1, 5, 6, 1)
        self.gridlayout.addWidget(self.label_customizationArea, 1, 6, 1, 1)

        # row 2
        self.gridlayout.addWidget(self.label_accountName, 2, 0, 1, 1)
        self.gridlayout.addWidget(self.lineEdit_accountName, 2, 1, 1, 2)
        self.gridlayout.addWidget(self.pushButton_deleteAccount, 2, 3, 1, 1)
        self.gridlayout.addWidget(self.pushButton_accountName, 2, 4, 1, 1)
        # col 5 empty
        self.gridlayout.addWidget(self.radioButton_mainNet, 2, 6, 1, 1)

        # row 3
        self.gridlayout.addWidget(self.label_activeAddress, 3, 0, 1, 1)
        self.gridlayout.addWidget(self.comboBox_activeAddressVal, 3, 1, 1, 3)
        self.gridlayout.addWidget(self.pushButton_copyAddress, 3, 4, 1, 1)
        # col 5 empty
        self.gridlayout.addWidget(self.radioButton_testNet, 3, 6, 1, 1)

        # row 4
        self.gridlayout.addWidget(self.label_amount, 4, 0, 1, 1)
        self.gridlayout.addWidget(self.label_amountVal, 4, 1, 1, 3)
        self.gridlayout.addWidget(self.pushButton_etherScan, 4, 4, 1, 1)
        # col 5 empty
        # col 6 empty

        # row 5
        self.gridlayout.addWidget(self.label_send, 5, 0, 1, 1)
        self.gridlayout.addWidget(self.lineEdit_send, 5, 1, 1, 3)
        self.gridlayout.addWidget(self.pushButton_send, 5, 4, 1, 1)
        # col 5 empty
        # col 6 empty

        # row 6
        self.gridlayout.addWidget(self.label_message, 6, 0, 1, 1)
        self.gridlayout.addWidget(self.lineEdit_message, 6, 1, 1, 1)
        self.gridlayout.addWidget(self.label_sendValue, 6, 2, 1, 1)
        # col 3 empty
        self.gridlayout.addWidget(self.lineEdit_sendValue, 6, 4, 1, 1)
        # col 5 empty
        # col 6 empty

        # row 7
        self.gridlayout.addWidget(self.textEdit_main, 7, 0, 1, 7)

        HEIGHT = 24
        self.label_nodeProvider.setMinimumHeight(HEIGHT)
        self.lineEdit_nodeProvider.setMinimumHeight(HEIGHT)
        self.pushButton_nodeProvider.setMinimumHeight(HEIGHT)

        self.label_accountName.setMinimumHeight(HEIGHT)
        self.lineEdit_accountName.setMinimumHeight(HEIGHT)
        self.pushButton_accountName.setMinimumHeight(HEIGHT)
        self.pushButton_deleteAccount.setMinimumHeight(HEIGHT)

        self.label_activeAddress.setMinimumHeight(HEIGHT)
        self.comboBox_activeAddressVal.setMinimumHeight(HEIGHT)
        self.pushButton_copyAddress.setMinimumHeight(HEIGHT)

        self.label_amount.setMinimumHeight(HEIGHT)
        self.label_amountVal.setMinimumHeight(HEIGHT)
        self.pushButton_etherScan.setMinimumHeight(HEIGHT)

        self.label_send.setMinimumHeight(HEIGHT)
        self.lineEdit_send.setMinimumHeight(HEIGHT)

        self.label_sendValue.setMinimumHeight(HEIGHT)
        self.lineEdit_sendValue.setMinimumHeight(HEIGHT)
        self.label_message.setMinimumHeight(HEIGHT)
        self.lineEdit_message.setMinimumHeight(HEIGHT)
        self.pushButton_send.setMinimumHeight(HEIGHT)

        MENU_HEIGHT = 16
        self.menu_wallet.setMinimumHeight(MENU_HEIGHT)
        self.menu_network.setMinimumHeight(MENU_HEIGHT)

        self.comboBox_activeAddressVal.clear()
        self.lineEdit_nodeProvider.setText('https://rpc.sepolia.org')
        self.radioButton_mainNet.setChecked(False)
        self.radioButton_testNet.setChecked(True)
        self.lineEdit_accountName.setEnabled(False)

    def initIcons(self):
        icon = QIcon()
        ICON_SIZE = 16

        # icon.addPixmap(QPixmap(system.getIconPath('copy_w.png')))
        # self.setWindowIcon(QtGui.QIcon('icon.png'))
        # self.setIconSize(QSize(ICON_SIZE, ICON_SIZE))

        self.pushButton_copyAddress.setIcon(QtGui.QIcon(system.getIconPath('copy.png')))
        self.pushButton_copyAddress.setIconSize(QSize(ICON_SIZE, ICON_SIZE))

        self.pushButton_etherScan.setIcon(QtGui.QIcon(system.getIconPath('ethereum.png')))
        self.pushButton_etherScan.setIconSize(QSize(ICON_SIZE, ICON_SIZE))

        self.pushButton_nodeProvider.setIcon(QtGui.QIcon(system.getIconPath('node.png')))
        self.pushButton_nodeProvider.setIconSize(QSize(ICON_SIZE, ICON_SIZE))

        self.pushButton_send.setIcon(QtGui.QIcon(system.getIconPath('moneyTransfer.png')))
        self.pushButton_send.setIconSize(QSize(ICON_SIZE, ICON_SIZE))

        self.pushButton_accountName.setIcon(QtGui.QIcon(system.getIconPath('edit.png')))
        self.pushButton_accountName.setIconSize(QSize(ICON_SIZE, ICON_SIZE))

        self.pushButton_deleteAccount.setIcon(QtGui.QIcon(system.getIconPath('delete.png')))
        self.pushButton_deleteAccount.setIconSize(QSize(ICON_SIZE, ICON_SIZE))

    def initStyleSheet(self):
        mainStyle = (
            "background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,"
            "stop:0 rgb(30, 76, 108) , stop:1 rgb(47, 54, 60));"
        )
        self.setStyleSheet(mainStyle)
        menuBarStyle = (
            "QMenuBar {background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,"
            "stop:0 rgb(47, 54, 60) , stop:1 rgb(30, 76, 108));"
            "spacing: 3 px;}"
            "QMenuBar::item {background: rgb(47, 54, 60);"
            "padding: 2px 25px 2px 20px; border: 1px solid rgb(108, 204, 244);; border-radius: 10px;}"
            "QMenuBar::item:selected {border: 2px solid rgb(108, 204, 244); background: rgb(30, 76, 108);}"
            "QMenuBar::item:pressed{background: rgb(108, 204, 244); color: black}"
        )
        self.menubar_file.setStyleSheet(menuBarStyle)
        menuStyle = (
            "QMenu {background-color: rgb(47, 54, 60); margin: 2px;}"
            "QMenu::item { padding: 2px 25px 2px 20px; border: 1px solid transparent; border-radius: 10px;}"
            "QMenu::item:selected {border: 2px solid rgb(108, 204, 244); background: rgb(30, 76, 108);}"
            "QMenu::item:pressed {background: rgb(108, 204, 244); color: black}"
        )
        self.menu_wallet.setStyleSheet(menuStyle)
        self.menu_network.setStyleSheet(menuStyle)
        buttonStyle = (
            "QPushButton {border: 2px solid rgb(108, 204, 244);"
            "border-radius: 12px;"
            "background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,"
            "stop:0 rgb(30, 76, 108) , stop:1 rgb(47, 54, 60));"
            "min-width: 80px;}"
            "QPushButton:hover {color: black; background-color: rgb(190, 200, 207);}"
            "QPushButton:pressed {background-color: rgb(108, 204, 244);}"
        )
        self.pushButton_send.setStyleSheet(buttonStyle)
        self.pushButton_etherScan.setStyleSheet(buttonStyle)
        self.pushButton_accountName.setStyleSheet(buttonStyle)
        self.pushButton_nodeProvider.setStyleSheet(buttonStyle)
        self.pushButton_copyAddress.setStyleSheet(buttonStyle)
        self.pushButton_deleteAccount.setStyleSheet(buttonStyle)
        labelStyle = (
            "color: white;"
            "background-color: transparent;"
        )
        self.label_send.setStyleSheet(labelStyle)
        self.label_message.setStyleSheet(labelStyle)
        self.label_amount.setStyleSheet(labelStyle)
        self.label_accountName.setStyleSheet(labelStyle)
        self.label_sendValue.setStyleSheet(labelStyle)
        self.label_activeAddress.setStyleSheet(labelStyle)
        self.label_customizationArea.setStyleSheet(labelStyle)
        self.label_nodeProvider.setStyleSheet(labelStyle)
        self.label_amountVal.setStyleSheet(labelStyle)
        self.label_amountVal.setText(
            '<span style = "color: red; font-weight: bold;" > 0'
            '</ span> <span style = "color: rgb(140, 170, 250); font-weight: bold;" > ETH </ span>')
        lineEditStyle = (
            "background-color: rgb(250, 240, 200); color: black"
        )
        self.lineEdit_nodeProvider.setStyleSheet(lineEditStyle)
        self.lineEdit_send.setStyleSheet(lineEditStyle)
        self.lineEdit_sendValue.setStyleSheet(lineEditStyle)
        self.lineEdit_message.setStyleSheet(lineEditStyle)
        self.lineEdit_accountName.setStyleSheet("background-color: transparent; border: none;"
                                                "color: rgb(108, 204, 244); font-weight: bold;")
        radioButtonStyle = (
            "QRadioButton {background-color: transparent;}"
            "QRadioButton::indicator { width: 24px; height: 12px; border-radius: 7px;}"
            "QRadioButton::indicator:unchecked{border: 1px solid red;}"
            "QRadioButton::indicator:checked{border: 1px solid green;background-image : url("
            f"{system.getIconPath('fill.png')})}}"
            "QRadioButton::indicator:checked:pressed{border: 1px solid white;}"
        )
        self.radioButton_testNet.setStyleSheet(radioButtonStyle)
        self.radioButton_mainNet.setStyleSheet(radioButtonStyle)

        self.comboBox_activeAddressVal.setStyleSheet(
            "background-color: rgb(30, 76, 108); color: black; "
            "selection-background-color: rgb(47, 54, 60); selection-color: white; "
        )
        self.textEdit_main.setStyleSheet("background-color: black; color: cyan")

    def setClickEvents(self):
        self.pushButton_copyAddress.clicked.connect(self.copyAddress)
        self.pushButton_etherScan.clicked.connect(self.goToEtherscan)
        self.pushButton_nodeProvider.clicked.connect(self.goToEtherNodes)
        self.pushButton_accountName.clicked.connect(self.editAccountName)
        self.pushButton_deleteAccount.clicked.connect(self.deleteAccount)
        self.pushButton_send.clicked.connect(self.sendTransaction)
        # Wallets-New wallet---------------------------------------------------------------------------------
        self.action_newRandomAccount.triggered.connect(self.createAccountRandom)
        self.action_recoverFromMnemonic.triggered.connect(self.createAccountFromMnemonic)
        self.action_recoverFromEntropy.triggered.connect(self.createAccountFromEntropy)
        self.action_recoverFromPrivateKey.triggered.connect(self.createAccountFromPrivateKey)
        # Wallets-Secrets---------------------------------------------------------------------------------
        self.action_entropy.triggered.connect(lambda: self.showSecrets(dataTypes.SECRET.ENTROPY))
        self.action_privateKey.triggered.connect(lambda: self.showSecrets(dataTypes.SECRET.PRIVATE_KEY))
        self.action_publicKeyCoordinates.triggered.connect(lambda: self.showSecrets(dataTypes.SECRET.PUBLIC_KEY_X))
        self.action_publicKey.triggered.connect(lambda: self.showSecrets(dataTypes.SECRET.PUBLIC_KEY))
        self.action_mnemonic.triggered.connect(lambda: self.showSecrets(dataTypes.SECRET.MNEMONIC))
        # Network-Transactions---------------------------------------------------------------------------------
        self.action_backup.triggered.connect(self.backupWallet)
        self.action_restore.triggered.connect(self.restoreWallet)
        # Network-Transactions---------------------------------------------------------------------------------
        self.action_checkTx.triggered.connect(self.showCustomTransaction)
        self.action_txNonce.triggered.connect(self.showNonce)
        self.action_simpleHistory.triggered.connect(self.showSimpleHistory)
        self.action_allNormal.triggered.connect(self.showNormalTransactions)
        self.action_allInternal.triggered.connect(self.showInternalTransactions)
        # Network-Tools---------------------------------------------------------------------------------
        self.action_publicKeyFromTxHash.triggered.connect(self.showSenderPublicKey)
        self.action_transactionMessage.triggered.connect(self.showCustomTransactionMessage)
        # ----------------------------------------------------------------------------------
        self.radioButton_mainNet.toggled.connect(self.changeNetwork)
        self.radioButton_testNet.toggled.connect(self.changeNetwork)
        # ----------------------------------------------------------------------------------
        self.lineEdit_sendValue.textChanged.connect(self.lineEditSendValueChange)
        self.comboBox_activeAddressVal.currentTextChanged.connect(self.comboBoxChange)

    def setMenuActions(self):
        self.action_newRandomAccount.setShortcut('Ctrl+n')
        self.action_newRandomAccount.setStatusTip('create new random account')
        self.action_recoverFromMnemonic.setShortcut('Ctrl+m')
        self.action_recoverFromMnemonic.setStatusTip('create new account from mnemonic')
        self.action_recoverFromEntropy.setShortcut('Ctrl+e')
        self.action_recoverFromEntropy.setStatusTip('create new account from entropy')
        self.action_recoverFromPrivateKey.setShortcut('Ctrl+p')
        self.action_recoverFromPrivateKey.setStatusTip('create new account from privateKey')
        # ----------------------------------------------------------------------------------
        self.action_entropy.setShortcut('Alt+e')
        self.action_entropy.setStatusTip('show account entropy')
        self.action_privateKey.setShortcut('Alt+v')
        self.action_privateKey.setStatusTip('show account privateKey')
        self.action_publicKeyCoordinates.setShortcut('Alt+c')
        self.action_publicKeyCoordinates.setStatusTip('show account publicKey coordinates')
        self.action_publicKey.setShortcut('Alt+p')
        self.action_publicKey.setStatusTip('show account publicKey')
        self.action_mnemonic.setShortcut('Alt+m')
        self.action_mnemonic.setStatusTip('show account mnemonic')
        # ----------------------------------------------------------------------------------

    def changeNetwork(self):
        try:
            if self.radioButton_mainNet.isChecked() and not self.radioButton_testNet.isChecked():
                self.lineEdit_nodeProvider.setText('https://nodes.mewapi.io/rpc/eth')
            elif not self.radioButton_mainNet.isChecked() and self.radioButton_testNet.isChecked():
                self.lineEdit_nodeProvider.setText('https://rpc.sepolia.org')
            else:
                raise
        except Exception as er:
            gui_errorDialog.Error('changeNetwork', str(er)).exec()

    def comboBoxChange(self):
        try:
            accountName = self.db.readColumnByCondition('NAM', self.comboBox_activeAddressVal.currentText())
            self.lineEdit_accountName.setText(str(accountName[0][0]))
        except Exception as er:
            gui_errorDialog.Error('comboBoxChange', str(er)).exec()

    def editAccountName(self):
        try:
            icon = QIcon()
            if self.pushButton_accountName.text() == 'Edit':
                self.lineEdit_accountName.setEnabled(True)
                self.lineEdit_accountName.setStyleSheet("background-color: rgb(250, 240, 200); color: black")
                self.pushButton_accountName.setText('Save')
                icon.addPixmap(QPixmap(system.getIconPath('save48.png')))
                self.pushButton_accountName.setIcon(icon)
                self.pushButton_nodeProvider.setIconSize(QSize(16, 16))
            elif self.pushButton_accountName.text() == 'Save':
                self.lineEdit_accountName.setEnabled(False)
                self.lineEdit_accountName.setStyleSheet(
                    "background-color: transparent; border: none;"
                    "color: rgb(108, 204, 244); font-weight: bold;")
                self.pushButton_accountName.setText('Edit')
                icon.addPixmap(QPixmap(system.getIconPath('edit40.png')))
                self.pushButton_accountName.setIcon(icon)
                self.pushButton_nodeProvider.setIconSize(QSize(16, 16))
                self.db.updateRowValue(columnName='NAM',
                                       newValue=self.lineEdit_accountName.text(),
                                       condition=self.comboBox_activeAddressVal.currentText())
            else:
                raise
        except Exception as er:
            gui_errorDialog.Error('editAccountName', str(er)).exec()

    def lineEditSendValueChange(self):
        try:
            if self.lineEdit_sendValue.text() == '':
                self.lineEdit_sendValue.setStyleSheet('background-color: rgb(250, 240, 200); color: black')
            else:
                OldValue = float(self.lineEdit_sendValue.text())
                OldMax = 1
                OldMin = 0.01
                NewMax = 65
                NewMin = 245
                OldRange = (OldMax - OldMin)
                NewRange = (NewMax - NewMin)
                NewValue = int((((OldValue - OldMin) * NewRange) / OldRange) + NewMin)
                if NewValue < 65:
                    NewValue = 65
                elif NewValue > 245:
                    NewValue = 245
                self.lineEdit_sendValue.setStyleSheet(f'background-color: rgb(245, {NewValue}, 65); color: black')
        except Exception as er:
            # gui_errorDialog.Error(str(er)).exec()
            pass  # nothing to do

    def createAccountRandom(self):
        try:
            userAnswer = True
            if self.db.isAccountExist():
                createAccount_window = qui_getUserChoice.Ui('Create new random account',
                                                            'Some account(s) already exist',
                                                            'Create new one?')
                createAccount_window.exec()
                userAnswer = createAccount_window.getAnswer()
            if not userAnswer:
                pass  # cancel by user or it is new account
            else:
                acc = account.New.random()  # create new account
                if not acc:
                    pass  # random account creation return by some error
                else:
                    if self.db.insertRow(acc):
                        self.comboBox_activeAddressVal.addItem(acc['address'])
                        self.comboBox_activeAddressVal.setCurrentIndex(self.comboBox_activeAddressVal.count() - 1)
                    else:
                        pass  # Inserting account details to database failed
        except Exception as er:
            gui_errorDialog.Error('createAccountRandom', str(er)).exec()

    def createAccountFromEntropy(self):
        try:
            getEntropy = qui_getUserInput.Ui('Recover account from entropy',
                                             'Enter your entropy:')
            getEntropy.exec()
            entropy = getEntropy.getInput()
            if entropy == '':
                qui_showMessage.Ui('Recover account from entropy', 'Nothing received',
                                   'you can try again from Wallet -> New account -> Recover from entropy').exec()
            else:
                acc = account.New.fromEntropy(entropy)
                if not acc:
                    pass  # Account creation failed
                else:
                    if self.db.insertRow(acc):
                        self.comboBox_activeAddressVal.addItem(acc['address'])
                        self.comboBox_activeAddressVal.setCurrentIndex(self.comboBox_activeAddressVal.count() - 1)
                    else:
                        pass  # Inserting account details to database failed
        except Exception as er:
            gui_errorDialog.Error('createAccountFromEntropy', str(er)).exec()

    def createAccountFromPrivateKey(self):
        try:
            getPrivateKey = qui_getUserInput.Ui('Recover account from privateKey',
                                                'Enter your private key:')
            getPrivateKey.exec()
            privateKey = getPrivateKey.getInput()
            if privateKey == '':
                qui_showMessage.Ui('Recover account from privateKey', 'Nothing received',
                                   'you can try again from Wallet -> New account -> Recover from private key').exec()
            else:
                acc = account.New.fromPrivateKey(privateKey)
                if not acc:
                    pass  # Account creation failed
                else:
                    if self.db.insertRow(acc):
                        self.comboBox_activeAddressVal.addItem(acc['address'])
                        self.comboBox_activeAddressVal.setCurrentIndex(self.comboBox_activeAddressVal.count() - 1)
                    else:
                        pass  # Inserting account details to database failed
        except Exception as er:
            gui_errorDialog.Error('createAccountFromPrivateKey', str(er)).exec()

    def createAccountFromMnemonic(self):
        try:
            getMnemonic = qui_getUserInput.Ui('Recover account from mnemonic', 'Enter your mnemonic:')
            getMnemonic.exec()
            mnemonic = getMnemonic.getInput()
            if mnemonic == '':
                qui_showMessage.Ui('Recover account from mnemonic', 'Nothing received',
                                   'you can try again from Wallet -> New account -> Recover from mnemonic').exec()
            else:
                acc = account.New.fromMnemonic(mnemonic)
                if not acc:
                    pass  # Account creation failed
                else:
                    if self.db.insertRow(acc):
                        self.comboBox_activeAddressVal.addItem(acc['address'])
                        self.comboBox_activeAddressVal.setCurrentIndex(self.comboBox_activeAddressVal.count() - 1)
                    else:
                        pass  # Inserting account details to database failed
        except Exception as er:
            gui_errorDialog.Error('createAccountFromMnemonic', str(er)).exec()

    def goToEtherscan(self):
        try:
            active_address = self.comboBox_activeAddressVal.currentText()
            if active_address is None:
                gui_errorDialog.Error('goToEtherscan', 'No address selected').exec()
            else:
                if self.radioButton_mainNet.isChecked() and not self.radioButton_testNet.isChecked():
                    web_browser_open('https://etherscan.io/address/' + active_address)
                elif not self.radioButton_mainNet.isChecked() and self.radioButton_testNet.isChecked():
                    web_browser_open('https://sepolia.etherscan.io/address/' + active_address)
                else:
                    gui_errorDialog.Error('goToEtherscan', 'Unknown network').exec()
        except Exception as er:
            gui_errorDialog.Error('goToEtherscan', str(er)).exec()

    def goToEtherNodes(self):
        try:
            if self.radioButton_mainNet.isChecked() and not self.radioButton_testNet.isChecked():
                web_browser_open('https://ethereumnodes.com/')
            elif not self.radioButton_mainNet.isChecked() and self.radioButton_testNet.isChecked():
                web_browser_open('https://sepolia.dev/')
            else:
                gui_errorDialog.Error('goToEtherNodes', 'Unknown network').exec()
        except Exception as er:
            gui_errorDialog.Error('goToEtherNodes', str(er)).exec()

    def copyAddress(self):
        try:
            active_address = self.comboBox_activeAddressVal.currentText()
            if active_address is not None:
                copy(active_address)
            # spam = pyperclip.paste()
        except Exception as er:
            gui_errorDialog.Error('copyAddress', str(er)).exec()

    def showSecrets(self, secretType: dataTypes.SECRET):
        try:
            self.textEdit_main.clear()
            if secretType == dataTypes.SECRET.ENTROPY and (
                    self.db.readColumnByCondition(
                        dataTypes.SECRET.ENTROPY.value, self.comboBox_activeAddressVal.currentText()
                    ) == self.db.readColumnByCondition(dataTypes.SECRET.PRIVATE_KEY.value,
                                                       self.comboBox_activeAddressVal.currentText())):
                qui_showMessage.Ui('Show secrets',
                                   'You have recovered an old account.',
                                   'Entropy is not recoverable from private key').exec()
            elif secretType == dataTypes.SECRET.MNEMONIC and (
                    self.db.readColumnByCondition(
                        dataTypes.SECRET.MNEMONIC.value, self.comboBox_activeAddressVal.currentText()
                    ) == self.db.readColumnByCondition(dataTypes.SECRET.PRIVATE_KEY.value,
                                                       self.comboBox_activeAddressVal.currentText())):
                qui_showMessage.Ui('Show secrets',
                                   'You have recovered an old account.',
                                   'Mnemonic is not recoverable from private key').exec()
            elif secretType == dataTypes.SECRET.PUBLIC_KEY_X or secretType == dataTypes.SECRET.PUBLIC_KEY_Y:
                result_X = self.db.readColumnByCondition(dataTypes.SECRET.PUBLIC_KEY_X.value,
                                                         self.comboBox_activeAddressVal.currentText())
                result_Y = self.db.readColumnByCondition(dataTypes.SECRET.PUBLIC_KEY_Y.value,
                                                         self.comboBox_activeAddressVal.currentText())
                if len(result_X) <= 0 or len(result_Y) <= 0:
                    gui_errorDialog.Error('showSecrets', 'Reading database failed').exec()
                elif len(result_X) == 1 or len(result_Y) == 1:
                    self.textEdit_main.append(f'Your account PUBLIC_KEY COORDINATE keep it safe:\n')
                    self.textEdit_main.append('X : ' + result_X[0][0])
                    self.textEdit_main.append('Y : ' + result_Y[0][0])
                else:
                    self.textEdit_main.append(f'Receiving unusual account PUBLIC_KEY COORDINATE:\n')
                    for res in result_X:
                        self.textEdit_main.append('X:' + res[0][0])
                    for res in result_Y:
                        self.textEdit_main.append('Y:' + res[0][0])
            else:
                result = self.db.readColumnByCondition(secretType.value,
                                                       self.comboBox_activeAddressVal.currentText())
                if len(result) <= 0:
                    gui_errorDialog.Error('showSecrets', 'Reading database failed').exec()
                elif len(result) == 1:
                    self.textEdit_main.append(f'Your account {secretType.name} keep it safe:\n')
                    self.textEdit_main.append(f'{result[0][0]}\n')
                    if secretType == dataTypes.SECRET.MNEMONIC or secretType == dataTypes.SECRET.ENTROPY:
                        self.textEdit_main.append(f'{secretType.name} + Passphrase = your account\n\n'
                                                  f'{secretType.name} without Passphrase = unknown account\n'
                                                  f'(If no passphrase set = your account)')
                    elif secretType == dataTypes.SECRET.PRIVATE_KEY:
                        self.textEdit_main.append(f'{secretType.name} = your account')
                else:
                    for res in result:
                        self.textEdit_main.append(f'{res[0]}\n')
        except Exception as er:
            gui_errorDialog.Error('showSecrets', str(er)).exec()

    def getBalance(self):
        try:
            if self.comboBox_activeAddressVal.count() == 0:
                pass  # no account available
            else:
                balance = ethereum.getBalance(self.comboBox_activeAddressVal.currentText(),
                                              self.lineEdit_nodeProvider.text())
                if balance < 0:
                    pass  # error in getting balance
                else:
                    color = 'red'
                    if balance > 0:
                        color = 'green'
                    self.label_amountVal.setText(
                        '<span style = "color: ' + color + '; font-weight: bold;" > ' + str(balance) +
                        '</ span> <span style = "color: rgb(140, 170, 250); font-weight: bold;" > ETH </ span>')
                    print('balance = ', balance)
        except Exception as er:
            gui_errorDialog.Error('getBalance', str(er)).exec()

    def sendTransaction(self, isContract: bool = False):
        if not self.lineEdit_message.text() == '' or not self.lineEdit_sendValue.text() == '':
            if self.lineEdit_send.text() == '' and isContract:  # deploy contract
                pass
            elif self.lineEdit_send.text() == '' and not isContract:  # send transaction need address
                qui_showMessage.Ui('sendTransaction', "Enter the recipient\'s address").exec()
                return {}
            else:
                if self.lineEdit_message.text() == '':  # it is normal transaction
                    if self.lineEdit_sendValue.text() == '':
                        qui_showMessage.Ui('sendTransaction', "Enter value to send").exec()
                        return {}
                    else:
                        self.sentETH()
                elif not self.lineEdit_message.text() == '':  # it is message transaction
                    self.sentETHMessage()
        else:
            qui_showMessage.Ui('sendTransaction', 'Please fill the required sections').exec()
            return {}

    def sentETH(self):
        try:
            transactions = self.transactionElements()
            if not transactions:
                pass  # error
            else:
                gas = ethereum.estimateGas(transactions)
                if not gas:
                    pass  # error
                senETH = qui_getUserChoice.Ui('Sending your money to others',
                                              f'Send {transactions["vale"]} ETH to {transactions["receiver"]}'
                                              f"\nestimated gas fee is:\n"
                                              f"Lowest = {gas['GasPrice']['low']} ETH\n"
                                              f"Median = {gas['GasPrice']['medium']} ETH\n"
                                              f"Highest = {gas['GasPrice']['high']} ETH\n",
                                              'Are you sure?')
                senETH.exec()
                if not senETH.getAnswer():  # cancel by user
                    qui_showMessage.Ui('I\'m entranced with joy',
                                       'You are in safe',
                                       'Nothing has been sent').exec()
                else:
                    transactionHash = ethereum.sendValueTransaction(privateKey=(self.db.readColumnByCondition(
                        dataTypes.SECRET.PRIVATE_KEY.value, transactions['sender']))[0][0], txElements=transactions)
                    if transactionHash == '':
                        pass  # Transaction failed
                    else:
                        qui_showMessage.Ui('Your job is done',
                                           'Transaction succeed:',
                                           f'Hash: {transactionHash}').exec()
                        self.showTransaction(transactionHash)
        except Exception as er:
            gui_errorDialog.Error('sentETH', str(er)).exec()

    def sentETHMessage(self):
        try:
            transactions = self.transactionElements(data=self.lineEdit_message.text().encode("utf-8").hex())
            if not transactions:
                pass  # error
            else:
                gas = ethereum.estimateGas(transactions)
                if not gas:
                    pass  # error
                senETH = qui_getUserChoice.Ui('Sending your message to others',
                                              f'Send {transactions["data"]}\n'
                                              f'to {transactions["receiver"]}'
                                              f"\nestimated gas fee is:\n"
                                              f"Lowest = {gas['GasPrice']['low']} ETH\n"
                                              f"Median = {gas['GasPrice']['medium']} ETH\n"
                                              f"Highest = {gas['GasPrice']['high']} ETH\n",
                                              'Are you sure?')
                senETH.exec()
                if not senETH.getAnswer():  # cancel by user
                    qui_showMessage.Ui('I\'m entranced with joy',
                                       'You are in safe',
                                       'Nothing has been sent').exec()
                else:
                    transactionHash = ethereum.sendMessageTransaction(privateKey=(self.db.readColumnByCondition(
                        dataTypes.SECRET.PRIVATE_KEY.value, transactions['sender']))[0][0], txElements=transactions)
                    if transactionHash == '':
                        pass  # Transaction failed
                    else:
                        qui_showMessage.Ui('Your job is done',
                                           'Transaction succeed:',
                                           f'Hash: {transactionHash}').exec()
                        self.showTransaction(transactionHash)
        except Exception as er:
            gui_errorDialog.Error('sentETH', str(er)).exec()

    def transactionElements(self, data: str = ''):
        try:
            if self.radioButton_mainNet.isChecked() and not self.radioButton_testNet.isChecked():
                chainId = 1  # Ethereum chain ID
            elif not self.radioButton_mainNet.isChecked() and self.radioButton_testNet.isChecked():
                chainId = 11155111  # Sepolia chain ID
            else:
                gui_errorDialog.Error('transactionElements', 'Unknown network').exec()
                chainId = 0
            if chainId > 0:
                if self.lineEdit_sendValue.text() == '':
                    val = 0
                else:
                    val = float(self.lineEdit_sendValue.text())
                return {
                    'sender': self.comboBox_activeAddressVal.currentText(),
                    'receiver': self.lineEdit_send.text(),
                    'vale': val,
                    'provider': self.lineEdit_nodeProvider.text(),
                    'chainId': chainId,
                    'data': data
                }
            else:
                pass  # network selection error
        except Exception as er:
            gui_errorDialog.Error('transactionElements', str(er)).exec()

    def showTransaction(self, txHash):
        try:
            tx = ethereum.getTransaction(txHash, self.lineEdit_nodeProvider.text())
            if tx == '':
                pass  # error getting transaction
            else:
                self.textEdit_main.clear()
                tx = loads(tx)  # convert to json
                for t in tx:
                    if tx[t] is None:
                        pass  # too soon
                    else:
                        if t == 'blockHash' or t == 'hash':
                            self.textEdit_main.append(f'{t} = {tx[t]}')
                        elif t == 'r' or t == 's':
                            self.textEdit_main.append(f"{t} = {int(tx[t], 0)}")
                        else:
                            self.textEdit_main.append(f'{t} = {tx[t]}')
                        cursor = QTextCursor(self.textEdit_main.document())
                        cursor.setPosition(0)
                        self.textEdit_main.setTextCursor(cursor)
        except Exception as er:
            gui_errorDialog.Error('showTransaction', str(er)).exec()

    def showTransactionMessage(self, txHash):
        try:
            tx = ethereum.getTransaction(txHash, self.lineEdit_nodeProvider.text())
            if tx == '':
                pass  # error getting transaction
            else:
                self.textEdit_main.clear()
                tx = loads(tx)  # convert to json
                self.textEdit_main.append(f"Transaction message is:\n\n"
                                          f" {bytearray.fromhex(tx['input'][2:]).decode('utf-8')}\n")
                self.textEdit_main.append('-' * 10)
                self.textEdit_main.append(f'transactionHash = {txHash}')
                for t in tx:
                    if t == 'blockNumber' or t == 'blockHash' or t == 'from' or t == 'to':
                        self.textEdit_main.append(f'{t} = {tx[t]}')
                    else:
                        pass
                cursor = QTextCursor(self.textEdit_main.document())
                cursor.setPosition(0)
                self.textEdit_main.setTextCursor(cursor)
        except Exception as er:
            gui_errorDialog.Error('showTransaction', str(er)).exec()

    def showCustomTransaction(self):
        try:
            TXHashWindow = qui_getUserInput.Ui('Show custom transaction',
                                               'Enter transaction hash:\n'
                                               '(Notice about mainNet and testNet)')
            TXHashWindow.exec()
            TXHash = TXHashWindow.getInput()
            if TXHash == '':
                qui_showMessage.Ui('Show custom transaction', 'Nothing received').exec()
            else:
                self.showTransaction(TXHash)
        except Exception as er:
            gui_errorDialog.Error('showCustomTransaction', str(er)).exec()

    def showCustomTransactionMessage(self):
        try:
            TXHashWindow = qui_getUserInput.Ui('Show custom transaction message',
                                               'Enter transaction hash:\n'
                                               '(Notice about mainNet and testNet)')
            TXHashWindow.exec()
            TXHash = TXHashWindow.getInput()
            if TXHash == '':
                qui_showMessage.Ui('Show custom transaction message', 'Nothing received').exec()
            else:
                self.showTransactionMessage(TXHash)
        except Exception as er:
            gui_errorDialog.Error('Show custom transaction message', str(er)).exec()

    def showNonce(self):
        try:
            nonce = ethereum.getAccountNonce(self.comboBox_activeAddressVal.currentText(),
                                             self.lineEdit_nodeProvider.text())
            if nonce < 0:
                pass  # error
            else:
                self.textEdit_main.clear()
                self.textEdit_main.append(f'Your current sent transaction count is {nonce}')
        except Exception as er:
            gui_errorDialog.Error('showNonce', str(er)).exec()

    def getNormalTransactions(self, APIkey: str) -> list:
        try:
            if self.radioButton_mainNet.isChecked() and not self.radioButton_testNet.isChecked():
                mainNet = True
            elif not self.radioButton_mainNet.isChecked() and self.radioButton_testNet.isChecked():
                mainNet = False
            else:
                gui_errorDialog.Error('getNormalTransactions', 'Unknown network').exec()
                return []

            txHistory = ethereum.getNormalHistory(self.comboBox_activeAddressVal.currentText(),
                                                  self.lineEdit_nodeProvider.text(), APIkey, mainNet)
            if not txHistory:
                return []  # error
            else:
                txHistory = loads(txHistory.decode('utf-8'))
                self.textEdit_main.clear()
                if not txHistory['status'] == '1' or not txHistory['message'] == 'OK':
                    gui_errorDialog.Error('getNormalTransactions',
                                          f'Bad response\n.'
                                          f' {txHistory}').exec()
                    return []
                else:
                    txHistory = txHistory['result']
                    return txHistory
        except Exception as er:
            gui_errorDialog.Error('getNormalTransactions', str(er)).exec()
            return []

    def getInternalTransactions(self, APIkey: str) -> list:
        try:
            if self.radioButton_mainNet.isChecked() and not self.radioButton_testNet.isChecked():
                mainNet = True
            elif not self.radioButton_mainNet.isChecked() and self.radioButton_testNet.isChecked():
                mainNet = False
            else:
                gui_errorDialog.Error('getInternalTransactions', 'Unknown network').exec()
                return []
            txHistory = ethereum.getInternalHistory(self.comboBox_activeAddressVal.currentText(),
                                                    self.lineEdit_nodeProvider.text(), APIkey, mainNet)
            if not txHistory:
                pass  # error
            else:
                txHistory = loads(txHistory.decode('utf-8'))
                self.textEdit_main.clear()
                if not txHistory['status'] == '1' or not txHistory['message'] == 'OK':
                    gui_errorDialog.Error('getInternalTransactions',
                                          f'Bad response\n.'
                                          f' {txHistory}').exec()
                    return []
                else:
                    txHistory = txHistory['result']
                    return txHistory
        except Exception as er:
            gui_errorDialog.Error('getInternalTransactions', str(er)).exec()
            return []

    def showSimpleHistory(self):
        try:
            TXHistoryWindow = qui_getUserInput.Ui('Show simple history',
                                                  'Enter your APIkey:\n'
                                                  '(Notice about mainNet and testNet)')
            TXHistoryWindow.exec()
            APIkey = TXHistoryWindow.getInput()
            if APIkey == '':
                qui_showMessage.Ui('Show simple history', 'Nothing received').exec()
            else:
                txHistoryNormal = self.getNormalTransactions(APIkey)
                txHistoryInternal = self.getInternalTransactions(APIkey)

                if len(txHistoryNormal) > 0 or len(txHistoryInternal) > 0:  # there is something for show
                    allTransactions = txHistoryNormal + txHistoryInternal
                    #  sort ace
                    sortedTransactions = sorted(allTransactions, key=lambda d: d['blockNumber'])
                    # de sort
                    sortedTransactions = sortedTransactions[::-1]
                    self.textEdit_main.append(f'Total {len(sortedTransactions)} transaction(s) received:\n'
                                              f'Offset is last 20000')
                    self.textEdit_main.append('-' * 10)
                    for n in sortedTransactions:
                        for e in n:
                            if e == 'blockNumber' or e == 'hash' or e == 'from' or e == 'to' or e == 'value':
                                if e == 'value':
                                    n[e] = float(n[e]) / 1000000000000000000
                                if e == 'to' and n[e] == '':
                                    n[e] = f"create contract by address {n['contractAddress']}"
                                self.textEdit_main.append(f'{str(e)} = {str(n[e])}')
                            else:
                                pass
                        self.textEdit_main.append('-' * 10)
                        cursor = QTextCursor(self.textEdit_main.document())
                        cursor.setPosition(0)
                        self.textEdit_main.setTextCursor(cursor)
                else:
                    pass  # error or there is no transaction
        except Exception as er:
            gui_errorDialog.Error('showSimpleHistory', str(er)).exec()

    def showNormalTransactions(self):
        try:
            TXHistoryWindow = qui_getUserInput.Ui('Show normal transactions',
                                                  'Enter your APIkey:\n'
                                                  '(Notice about mainNet and testNet)')
            TXHistoryWindow.exec()
            APIkey = TXHistoryWindow.getInput()
            if APIkey == '':
                qui_showMessage.Ui('Show normal transactions', 'Nothing received').exec()
            else:
                txHistory = self.getNormalTransactions(APIkey)
                if len(txHistory) == 0:
                    pass  # error or no transaction
                else:
                    self.textEdit_main.append(f'Total {len(txHistory)} transaction(s) received:\n'
                                              f'Offset is last 10000')
                    self.textEdit_main.append('-' * 10)
                    for n in txHistory:
                        for e in n:
                            self.textEdit_main.append(f'{str(e)} = {str(n[e])}')
                        self.textEdit_main.append('-' * 10)
                        cursor = QTextCursor(self.textEdit_main.document())
                        cursor.setPosition(0)
                        self.textEdit_main.setTextCursor(cursor)
        except Exception as er:
            gui_errorDialog.Error('showNormalTransactions', str(er)).exec()

    def showInternalTransactions(self):
        try:
            TXHistoryWindow = qui_getUserInput.Ui('Show internal transactions',
                                                  'Enter your APIkey:\n'
                                                  '(Notice about mainNet and testNet)')
            TXHistoryWindow.exec()
            APIkey = TXHistoryWindow.getInput()
            if APIkey == '':
                qui_showMessage.Ui('Show internal transactions', 'Nothing received').exec()
            else:
                txHistory = self.getInternalTransactions(APIkey)
                if len(txHistory) == 0:
                    pass  # error or no transactions
                else:
                    self.textEdit_main.clear()
                    self.textEdit_main.append(f'Total {len(txHistory)} transaction(s) received:\n'
                                              f'Offset is last 10000')
                    self.textEdit_main.append('-' * 10)
                    for n in txHistory:
                        for e in n:
                            self.textEdit_main.append(f'{str(e)} = {str(n[e])}')
                        self.textEdit_main.append('-' * 10)
                    cursor = QTextCursor(self.textEdit_main.document())
                    cursor.setPosition(0)
                    self.textEdit_main.setTextCursor(cursor)
        except Exception as er:
            gui_errorDialog.Error('showInternalTransactions', str(er)).exec()

    def showSenderPublicKey(self):
        try:
            TxHashWindow = qui_getUserInput.Ui('Show sender publicKey',
                                               'Enter transaction hash:\n'
                                               '(You will get sender publicKey and address)')
            TxHashWindow.exec()
            TxHash = TxHashWindow.getInput()
            if TxHash == '':
                (qui_showMessage.Ui('Show sender publicKey', 'Nothing received').exec())
            else:
                result = ethereum.getPublicKeyFromTransaction(TxHash, self.lineEdit_nodeProvider.text())
                if not result:
                    pass  # Error
                else:
                    self.textEdit_main.clear()
                    self.textEdit_main.append(f"\nSender address: {result['address']}\n"
                                              f"Sender publicKey: {result['publicKey']}")
                    cursor = QTextCursor(self.textEdit_main.document())
                    cursor.setPosition(0)
                    self.textEdit_main.setTextCursor(cursor)
        except Exception as er:
            gui_errorDialog.Error('showSenderPublicKey', str(er)).exec()

    def backupWallet(self):
        try:
            rowData = self.db.readRowByCondition(self.comboBox_activeAddressVal.currentText())[0]
            data = {'entropy': rowData[0],
                    'privateKey': rowData[1],
                    'publicKeyCoordinate': (rowData[2], rowData[3]),
                    'publicKey': rowData[4],
                    'address': rowData[5],
                    'mnemonic': rowData[6],
                    'Name': rowData[7]}
            WriteOnFile = False
            folderSelected = ''
            root = Tk()
            root.withdraw()
            folderSelected = filedialog.askdirectory()
            print(folderSelected)
            if not folderSelected:
                pass  # cancel by user
            else:
                passwordWindow = qui_getUserInput.Ui('backupWallet',
                                                     'Exporting the secrets of your account to the file.\n'
                                                     'For more security set a password on the file\n'
                                                     'or cancel for skip password protection')
                passwordWindow.exec()
                password = passwordWindow.getInput()
                if password == '':  # no password
                    if Path(f'{folderSelected}/{rowData[7].replace(" ", "_")}.json').is_file():
                        reWriteWindow = qui_getUserChoice.Ui('backupWallet',
                                                             'File is exist!',
                                                             'Overwrite it?')

                        reWriteWindow.exec()
                        WriteOnFile = reWriteWindow.getAnswer()
                    else:
                        WriteOnFile = True
                    if WriteOnFile:
                        with open(f'{folderSelected}/{rowData[7].replace(" ", "_")}.json', 'w+') as fp:
                            dump(data, fp)
                    else:
                        pass  # cancel by user
                else:
                    if Path(f'{folderSelected}/{rowData[7].replace(" ", "_")}.wallet').is_file():
                        reWriteWindow = qui_getUserChoice.Ui('backupWallet',
                                                             'File is exist!',
                                                             'Overwrite it?')

                        reWriteWindow.exec()
                        WriteOnFile = reWriteWindow.getAnswer()
                    else:
                        WriteOnFile = True
                    if WriteOnFile:
                        b_password = password.encode('utf-8')
                        b_data = dumps(data, indent=2).encode('utf-8')
                        encrypted = DES.encrypt(b_password, b_data)
                        with open(f'{folderSelected}/{rowData[7].replace(" ", "_")}.wallet', 'w+') as fp:
                            dump(encrypted, fp)
                    else:
                        pass  # cancel by user
        except Exception as er:
            gui_errorDialog.Error('backupWallet', str(er)).exec()

    def restoreWallet(self):
        try:
            root = Tk()
            root.withdraw()
            filePath = filedialog.askopenfilename()
            with open(filePath, 'r') as f:  # open the file
                data = f.readlines()[0]
            if filePath.endswith('.json'):  # non encrypted file
                jsonData = loads(data)
                if self.db.insertRow(jsonData):
                    self.comboBox_activeAddressVal.addItem(jsonData['address'])
                    self.comboBox_activeAddressVal.setCurrentIndex(self.comboBox_activeAddressVal.count() - 1)
                    self.lineEdit_accountName.setText(jsonData['Name'])
            elif filePath.endswith('.wallet'):  # an encrypted file
                passwordWindow = qui_getUserInput.Ui('restoreWallet',
                                                     'This is an encrypted file.\n'
                                                     "Enter the file password:\n")
                passwordWindow.exec()
                password = passwordWindow.getInput()
                if password == '':  # no password
                    gui_errorDialog.Error('restoreWallet', f'Nothing received\n'
                                                           f'{filePath}').exec()
                else:
                    decrypted = DES.decrypt(password.encode('utf-8'), data)
                    jsonData = loads(decrypted.decode('utf-8'))
                    self.showWallet(jsonData, filePath)
                    if self.db.insertRow(jsonData):
                        self.comboBox_activeAddressVal.addItem(jsonData['address'])
                        self.comboBox_activeAddressVal.setCurrentIndex(self.comboBox_activeAddressVal.count() - 1)
                        self.lineEdit_accountName.setText(jsonData['Name'])
            else:
                gui_errorDialog.Error('restoreWallet', f'Unknown file format\n'
                                                       f'{filePath}').exec()
        except Exception as er:
            gui_errorDialog.Error('restoreWallet', str(er)).exec()

    def showWallet(self, jsonData: dict, path: str):
        try:
            self.textEdit_main.clear()
            self.textEdit_main.append(f'New account from {path} loaded:')
            self.textEdit_main.append('-' * 10)
            for key in jsonData:
                self.textEdit_main.append(f'{key} = {jsonData[key]}')
            self.textEdit_main.append('-' * 10)
            cursor = QTextCursor(self.textEdit_main.document())
            cursor.setPosition(0)
            self.textEdit_main.setTextCursor(cursor)
        except Exception as er:
            gui_errorDialog.Error('showWallet', str(er)).exec()

    def deleteAccount(self):
        try:
            accountToDelete = self.comboBox_activeAddressVal.currentText()
            accountIndex = self.comboBox_activeAddressVal.currentIndex()
            accountName = self.lineEdit_accountName.text()
            deleteIt = False
            deleteWindow = qui_getUserChoice.Ui('deleteAccount',
                                                f'Delete account \"{accountName}\"?\n'
                                                f'account address: {accountToDelete}\n',
                                                'You will lost that\n'
                                                'Proceed?')

            deleteWindow.exec()
            deleteIt = deleteWindow.getAnswer()
            if not deleteIt:
                qui_showMessage.Ui('deleteAccount', 'Nothing has been removed.').exec()
            else:
                if self.db.deleteRow(self.comboBox_activeAddressVal.currentText()):
                    if self.comboBox_activeAddressVal.count() == 1:
                        self.comboBox_activeAddressVal.clear()
                    else:
                        self.comboBox_activeAddressVal.removeItem(accountIndex)
                    qui_showMessage.Ui('deleteAccount', 'the account was deleted.').exec()
                else:
                    pass  # error
        except Exception as er:
            gui_errorDialog.Error('deleteAccount', str(er)).exec()
