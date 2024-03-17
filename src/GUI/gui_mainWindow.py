from PyQt6.QtWebEngineWidgets import QWebEngineView
from pyperclip import copy
from PyQt6.QtWidgets import QFrame, QTabWidget
from json import loads, dump, dumps
from PyQt6 import QtWidgets, QtGui
from PyQt6.QtCore import QSize, QRect, QUrl
from PyQt6.QtGui import QAction, QTextCursor
from pathlib import Path
from tkinter import filedialog, Tk
from src.cryptography import DES
from src.GUI import gui_userChoice, gui_userInput, gui_error, gui_message
from src.validators import checkHex, checkURL
from PyQt6.QtWidgets import (QWidget, QGridLayout, QLabel, QPushButton, QComboBox, QLineEdit,
                             QRadioButton, QTextEdit, QMenuBar, QMenu, QStatusBar)
from src import (database, dataTypes, ethereum,
                 account, system)

ITEM_HEIGHT = 25
MENU_HEIGHT = 16
ICON_SIZE = 16
SEPOLIA_PROVIDER = "https://rpc-sepolia.rockx.com/"
ETHEREUM_PROVIDER = "https://nodes.mewapi.io/rpc/eth"
MAIN_WIDTH = 800
MAIN_HEIGHT = 600
SIDE_TAB_WIDTH = 25
SIDE_TAB_MARGIN = 2


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
        # menubar -------------------------------------------------------------------------
        self.action_newRandomAccount = QAction(self)
        self.action_recoverFromMnemonic = QAction(self)
        self.action_recoverFromEntropy = QAction(self)
        self.action_recoverFromPrivateKey = QAction(self)
        # ----------------------------------------------------------------------------------
        self.action_entropy = QAction(self)
        self.action_privateKey = QAction(self)
        self.action_publicKeyCoordinates = QAction(self)
        self.action_publicKey = QAction(self)
        self.action_mnemonic = QAction(self)
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
        self.action_pendingTransactions = QAction(self)
        # ----------------------------------------------------------------------------------
        # main tab widget
        self.centralWidget_main = QWidget(self)
        self.tabWidget_main = QTabWidget(self.centralWidget_main)
        # tab accounts
        self.tab_accounts = QWidget()
        self.gridLayoutWidget_accounts = QWidget(self.tab_accounts)
        self.gridlayout_accounts = QGridLayout(self.gridLayoutWidget_accounts)
        # tab tokens
        self.tab_tokens = QWidget()
        self.gridLayoutWidget_tokens = QWidget(self.tab_tokens)
        self.gridlayout_tokens = QGridLayout(self.gridLayoutWidget_tokens)
        # tab contract
        self.tab_contract = QWidget()
        self.gridLayoutWidget_contract = QWidget(self.tab_contract)
        self.gridlayout_contract = QGridLayout(self.gridLayoutWidget_contract)
        # tab NFT
        self.tab_nft = QWidget()
        self.gridLayoutWidget_nft = QWidget(self.tab_nft)
        self.gridlayout_nft = QGridLayout(self.gridLayoutWidget_nft)
        # tab webView
        self.tab_webView = QWidget()
        self.gridLayoutWidget_webView = QWidget(self.tab_webView)
        self.gridlayout_webView = QGridLayout(self.gridLayoutWidget_webView)
        # tab accounts  --------------------------------------------------------------------
        # row 1
        self.label_nodeProvider = QLabel(self.gridLayoutWidget_accounts)
        self.lineEdit_nodeProvider = QLineEdit(self.gridLayoutWidget_accounts)
        self.pushButton_nodeProvider = QPushButton(self.gridLayoutWidget_accounts)

        # row 2
        self.label_accountName = QLabel(self.gridLayoutWidget_accounts)
        self.lineEdit_accountName = QLineEdit(self.gridLayoutWidget_accounts)
        self.pushButton_accountName = QPushButton(self.gridLayoutWidget_accounts)
        self.pushButton_deleteAccount = QPushButton(self.gridLayoutWidget_accounts)

        # row 3
        self.label_activeAddress = QLabel(self.gridLayoutWidget_accounts)
        self.comboBox_activeAddressVal = QComboBox(self.gridLayoutWidget_accounts)
        self.pushButton_copyAddress = QPushButton(self.gridLayoutWidget_accounts)

        # row 4
        self.label_amount = QLabel(self.gridLayoutWidget_accounts)
        self.label_amountVal = QLabel(self.gridLayoutWidget_accounts)
        self.pushButton_etherScan = QPushButton(self.gridLayoutWidget_accounts)

        # row 5
        self.label_sendAddress = QLabel(self.gridLayoutWidget_accounts)
        self.lineEdit_sendAddress = QLineEdit(self.gridLayoutWidget_accounts)
        self.pushButton_send = QPushButton(self.gridLayoutWidget_accounts)

        # row 6
        self.label_sendValue = QLabel(self.gridLayoutWidget_accounts)
        self.lineEdit_sendValue = QLineEdit(self.gridLayoutWidget_accounts)
        self.label_message = QLabel(self.gridLayoutWidget_accounts)
        self.lineEdit_message = QLineEdit(self.gridLayoutWidget_accounts)

        # row 7
        self.textEdit_main = QTextEdit(self.gridLayoutWidget_accounts)

        # customization
        self.label_customizationArea = QLabel(self.gridLayoutWidget_accounts)
        self.radioButton_mainNet = QRadioButton(self.gridLayoutWidget_accounts)
        self.radioButton_testNet = QRadioButton(self.gridLayoutWidget_accounts)
        self.label_GasFeePriority = QLabel(self.gridLayoutWidget_accounts)
        self.comboBox_GasFeePriority = QComboBox(self.gridLayoutWidget_accounts)

        self.line_vertical = QFrame(self.gridLayoutWidget_accounts)
        #  tab webView ---------------------------------------------------------------------
        self.webEngineView = QWebEngineView(self.gridLayoutWidget_webView)

        self.statusbar = QStatusBar(self)

        self.db = database.Sqlite(dbName)
        self.transactionResult = {'message': '', 'hash': '', 'pending': 0}
        self.initUI()
        self.initIcons()
        self.initStyleSheet()
        self.setClickEvents()
        self.setMenuActionsTips()

    def initUI(self):
        self.setCentralWidget(self.centralWidget_main)
        self.resize(MAIN_WIDTH, MAIN_HEIGHT)
        self.setFixedSize(MAIN_WIDTH, MAIN_HEIGHT)
        self.setObjectName("MainWindow")
        self.setWindowTitle("FAwallet")
        self.centralWidget_main.setObjectName("centralWidget_main")
        self.tabWidget_main.setObjectName("tabWidget_main")
        self.tabWidget_main.setGeometry(QRect(0, 0, MAIN_WIDTH - SIDE_TAB_WIDTH, MAIN_HEIGHT))
        self.setMenuBar(self.menubar_file)
        # menubar -------------------------------------------------------------------------
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
        self.action_pendingTransactions.setObjectName('action_pendingTransactions ')
        # ----------------------------------------------------------------------------------
        self.menubar_file.setObjectName("menubar_file")
        self.menubar_file.setGeometry(QRect(0, 0, MAIN_WIDTH - SIDE_TAB_WIDTH, 25))
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
        self.menu_tools.addAction(self.action_pendingTransactions)
        self.action_pendingTransactions.setText('pending transactions')
        # ----------------------------------------------------------------------------------
        self.tabWidget_main.setTabPosition(QTabWidget.TabPosition.West)
        #  tabs  ---------------------------------------------------------------------------
        #  tab accounts
        self.tabWidget_main.addTab(self.tab_accounts, "Accounts")
        self.tab_accounts.setObjectName("tab_accounts")
        self.gridLayoutWidget_accounts.setObjectName("gridLayoutWidget_accounts")
        self.gridLayoutWidget_accounts.setGeometry(QRect(
            0, 0, MAIN_WIDTH - (2 * SIDE_TAB_WIDTH), MAIN_HEIGHT - ITEM_HEIGHT - MENU_HEIGHT))
        self.gridlayout_accounts.setObjectName("gridlayout_accounts")
        self.gridlayout_accounts.setGeometry(QRect(
            0, 0, MAIN_WIDTH - (2 * SIDE_TAB_WIDTH), MAIN_HEIGHT - ITEM_HEIGHT - MENU_HEIGHT))

        #  tab tokens
        self.tabWidget_main.addTab(self.tab_tokens, "Tokens")
        self.tab_tokens.setObjectName("tab_tokens")
        self.gridLayoutWidget_tokens.setObjectName("gridLayoutWidget_tokens")
        self.gridLayoutWidget_tokens.setGeometry(QRect(
            0, 0, MAIN_WIDTH - (2 * SIDE_TAB_WIDTH), MAIN_HEIGHT - ITEM_HEIGHT - MENU_HEIGHT))
        self.gridlayout_tokens.setObjectName("gridlayout_tokens")
        self.gridlayout_tokens.setGeometry(QRect(
            0, 0, MAIN_WIDTH - (2 * SIDE_TAB_WIDTH), MAIN_HEIGHT - ITEM_HEIGHT - MENU_HEIGHT))

        # tab contract
        self.tabWidget_main.addTab(self.tab_contract, "Contract")
        self.tab_contract.setObjectName("tab_contract")
        self.gridLayoutWidget_contract.setObjectName("gridLayoutWidget_contract")
        self.gridLayoutWidget_contract.setGeometry(QRect(
            0, 0, MAIN_WIDTH - (2 * SIDE_TAB_WIDTH), MAIN_HEIGHT - ITEM_HEIGHT - MENU_HEIGHT))
        self.gridlayout_contract.setObjectName("gridlayout_contract")
        self.gridlayout_contract.setGeometry(QRect(
            0, 0, MAIN_WIDTH - (2 * SIDE_TAB_WIDTH), MAIN_HEIGHT - ITEM_HEIGHT - MENU_HEIGHT))

        # tab nft
        self.tabWidget_main.addTab(self.tab_nft, "NFT")
        self.tab_nft.setObjectName("tab_nft")
        self.gridLayoutWidget_nft.setObjectName("gridLayoutWidget_nft")
        self.gridLayoutWidget_nft.setGeometry(QRect(
            0, 0, MAIN_WIDTH - (2 * SIDE_TAB_WIDTH), MAIN_HEIGHT - ITEM_HEIGHT - MENU_HEIGHT))
        self.gridlayout_nft.setObjectName("gridlayout_nft")
        self.gridlayout_nft.setGeometry(QRect(
            0, 0, MAIN_WIDTH - (2 * SIDE_TAB_WIDTH), MAIN_HEIGHT - ITEM_HEIGHT - MENU_HEIGHT))

        # tab webView
        self.tabWidget_main.addTab(self.tab_webView, "WebView")
        self.tab_webView.setObjectName("tab_webView")
        self.gridLayoutWidget_webView.setObjectName("gridLayoutWidget_webView")
        self.gridLayoutWidget_webView.setGeometry(QRect(
            0, 0, MAIN_WIDTH - (2 * SIDE_TAB_WIDTH), MAIN_HEIGHT - ITEM_HEIGHT - MENU_HEIGHT))
        self.gridlayout_webView.setObjectName("gridlayout_webView")
        self.gridlayout_webView.setGeometry(QRect(
            0, 0, MAIN_WIDTH - (2 * SIDE_TAB_WIDTH), MAIN_HEIGHT - ITEM_HEIGHT - MENU_HEIGHT))

        # accounts -------------------------------------------------------------------------
        # row 1
        self.label_nodeProvider.setObjectName("label_nodeProvider")
        self.label_nodeProvider.setText("Node provider:")
        self.lineEdit_nodeProvider.setText(ETHEREUM_PROVIDER)
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
        self.pushButton_deleteAccount.setText('Delete account')

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
        self.label_sendAddress.setObjectName("label_send")
        self.label_sendAddress.setText("Send ETH to:")
        self.lineEdit_sendAddress.setObjectName("lineEdit_send")
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
        self.label_GasFeePriority.setObjectName("label_GasFeePriority")
        self.label_GasFeePriority.setText("Transaction priority")
        self.comboBox_GasFeePriority.setObjectName("comboBox_GasFeePriority")
        self.comboBox_GasFeePriority.addItem('high')
        self.comboBox_GasFeePriority.addItem('medium')
        self.comboBox_GasFeePriority.addItem('low')
        self.comboBox_GasFeePriority.setCurrentIndex(1)

        self.line_vertical.setObjectName("line_vertical")
        self.line_vertical.setFrameShape(QFrame.Shape.VLine)

        # ----------------------------------------------------------------------------------
        self.setStatusBar(self.statusbar)
        self.statusbar.setObjectName("statusbar")
        # ----------------------------------------------------------------------------------
        # row 1
        self.gridlayout_accounts.addWidget(self.label_nodeProvider, 1, 0, 1, 1)
        self.gridlayout_accounts.addWidget(self.lineEdit_nodeProvider, 1, 1, 1, 3)
        self.gridlayout_accounts.addWidget(self.pushButton_nodeProvider, 1, 4, 1, 1)
        self.gridlayout_accounts.addWidget(self.line_vertical, 1, 5, 6, 1)
        self.gridlayout_accounts.addWidget(self.label_customizationArea, 1, 6, 1, 1)

        # row 2
        self.gridlayout_accounts.addWidget(self.label_accountName, 2, 0, 1, 1)
        self.gridlayout_accounts.addWidget(self.lineEdit_accountName, 2, 1, 1, 2)
        self.gridlayout_accounts.addWidget(self.pushButton_accountName, 2, 3, 1, 1)
        self.gridlayout_accounts.addWidget(self.pushButton_deleteAccount, 2, 4, 1, 1)
        # col 5 empty
        self.gridlayout_accounts.addWidget(self.radioButton_mainNet, 2, 6, 1, 1)

        # row 3
        self.gridlayout_accounts.addWidget(self.label_activeAddress, 3, 0, 1, 1)
        self.gridlayout_accounts.addWidget(self.comboBox_activeAddressVal, 3, 1, 1, 3)
        self.gridlayout_accounts.addWidget(self.pushButton_copyAddress, 3, 4, 1, 1)
        # col 5 empty
        self.gridlayout_accounts.addWidget(self.radioButton_testNet, 3, 6, 1, 1)

        # row 4
        self.gridlayout_accounts.addWidget(self.label_amount, 4, 0, 1, 1)
        self.gridlayout_accounts.addWidget(self.label_amountVal, 4, 1, 1, 3)
        self.gridlayout_accounts.addWidget(self.pushButton_etherScan, 4, 4, 1, 1)
        # col 5 empty
        self.gridlayout_accounts.addWidget(self.label_GasFeePriority, 4, 6, 1, 1)

        # row 5
        self.gridlayout_accounts.addWidget(self.label_sendAddress, 5, 0, 1, 1)
        self.gridlayout_accounts.addWidget(self.lineEdit_sendAddress, 5, 1, 1, 3)
        self.gridlayout_accounts.addWidget(self.pushButton_send, 5, 4, 1, 1)
        # col 5 empty
        self.gridlayout_accounts.addWidget(self.comboBox_GasFeePriority, 5, 6, 1, 1)

        # row 6
        self.gridlayout_accounts.addWidget(self.label_sendValue, 6, 0, 1, 1)
        self.gridlayout_accounts.addWidget(self.lineEdit_sendValue, 6, 1, 1, 1)
        self.gridlayout_accounts.addWidget(self.label_message, 6, 2, 1, 1)
        self.gridlayout_accounts.addWidget(self.lineEdit_message, 6, 3, 1, 2)
        # col 5 empty
        # col 6 empty

        # row 7
        self.gridlayout_accounts.addWidget(self.textEdit_main, 7, 0, 1, 7)

        self.label_nodeProvider.setMinimumHeight(ITEM_HEIGHT)
        self.lineEdit_nodeProvider.setMinimumHeight(ITEM_HEIGHT)
        self.pushButton_nodeProvider.setMinimumHeight(ITEM_HEIGHT)

        self.label_accountName.setMinimumHeight(ITEM_HEIGHT)
        self.lineEdit_accountName.setMinimumHeight(ITEM_HEIGHT)
        self.pushButton_accountName.setMinimumHeight(ITEM_HEIGHT)
        self.pushButton_deleteAccount.setMinimumHeight(ITEM_HEIGHT)

        self.label_activeAddress.setMinimumHeight(ITEM_HEIGHT)
        self.comboBox_activeAddressVal.setMinimumHeight(ITEM_HEIGHT)
        self.pushButton_copyAddress.setMinimumHeight(ITEM_HEIGHT)

        self.label_amount.setMinimumHeight(ITEM_HEIGHT)
        self.label_amountVal.setMinimumHeight(ITEM_HEIGHT)
        self.pushButton_etherScan.setMinimumHeight(ITEM_HEIGHT)

        self.label_sendAddress.setMinimumHeight(ITEM_HEIGHT)
        self.lineEdit_sendAddress.setMinimumHeight(ITEM_HEIGHT)

        self.label_sendValue.setMinimumHeight(ITEM_HEIGHT)
        self.lineEdit_sendValue.setMinimumHeight(ITEM_HEIGHT)
        self.label_message.setMinimumHeight(ITEM_HEIGHT)
        self.lineEdit_message.setMinimumHeight(ITEM_HEIGHT)
        self.pushButton_send.setMinimumHeight(ITEM_HEIGHT)

        self.menu_wallet.setMinimumHeight(MENU_HEIGHT)
        self.menu_network.setMinimumHeight(MENU_HEIGHT)

        self.label_GasFeePriority.setMinimumHeight(MENU_HEIGHT)
        self.comboBox_GasFeePriority.setMinimumHeight(MENU_HEIGHT)

        self.comboBox_activeAddressVal.clear()
        self.lineEdit_nodeProvider.setText(SEPOLIA_PROVIDER)
        self.radioButton_mainNet.setChecked(False)
        self.radioButton_testNet.setChecked(True)
        self.lineEdit_accountName.setEnabled(False)
        # webView  -------------------------------------------------------------------------
        self.webEngineView.setObjectName("webEngineView")
        self.webEngineView.setUrl(QUrl("https://etherscan.io/"))
        self.gridlayout_webView.addWidget(self.webEngineView, 0, 0, 1, 1)

    def initIcons(self):
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
            # "font-size:14px; "
            "margin: 0px  0px 0px 0px;"
            "padding: 0px 0px 0px 0px;"  # top, bottom, x ,x"
        )
        self.setStyleSheet(mainStyle)
        menuBarStyle = (
            "QMenuBar {background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,"
            "stop:0 rgb(47, 54, 60) , stop:1 rgb(30, 76, 108));"
            "spacing: 3 px;}"
            "QMenuBar::item {"
            # "height: 40px;"
            # "width: 40px;"
            "background: rgb(47, 54, 60);"
            "border: 1px solid rgb(108, 204, 244);"
            # "border-radius: 10px;"
            # "border-top-right-radius: 10px;"
            # "border-bottom-right-radius: 10px;"
            "padding: 3px 3px 3px 3px;"  # top, right, bottom, left
            "margin: 5px 0px 0px 3px;"  # top, right, bottom, left
            "}"
            "QMenuBar::item:selected {border: 2px solid rgb(108, 204, 244);"
            "background: rgb(30, 76, 108); "
            "border-radius: 10px;"
            "}"
            "QMenuBar::item:pressed{background: rgb(108, 204, 244); color: black}"
        )
        self.menubar_file.setStyleSheet(menuBarStyle)
        menuStyle = (
            "QMenu {background-color: rgb(47, 54, 60); margin: 2px;}"
            "QMenu::item { padding: 2px 25px 2px 20px;  "
            "border-top-left-radius: 10px;}"
            "QMenu::item:selected {border: 2px solid rgb(108, 204, 244); background: rgb(30, 76, 108);}"
            "QMenu::item:pressed {background: rgb(108, 204, 244); color: black}"
        )
        self.menu_wallet.setStyleSheet(menuStyle)
        self.menu_network.setStyleSheet(menuStyle)

        tabWidgetStyle = (
            "QTabWidget::pane { border: transparent;}"
            "QTabWidget::tab-bar {top: 217px;}"
            "QTabBar::tab:!selected {"
            "background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,"
            "stop:0 rgb(30, 76, 108) , stop:1 rgb(47, 54, 60));"
            "border: 1px solid  rgb(108, 204, 244);"
            "border-top-left-radius: 10px;"
            "border-bottom-right-radius: 10px;"
            f"height: 62px; width: {SIDE_TAB_WIDTH}px;"
            "padding: 0px 0px 0px 0px;"  # top, right, bottom, left
            "margin: 0px 0px 3px 3px;}"  # top, right, bottom, left
            "QTabBar::tab:!selected:hover {background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,"
            "stop:0 rgb(47, 54, 60) , stop:1 rgb(30, 76, 108));"
            # "border-top-right-radius: 10px;"
            # "border-bottom-left-radius: 10px;"
            # "border-top-left-radius: 0px;"
            # "border-bottom-right-radius: 0px;"
            "font-weight: bold;}"
            "QTabBar::tab:selected {background-color: rgb(47, 54, 60);"
            "border: 1px solid  rgb(108, 204, 244);"
            "border-top-left-radius: 10px;"
            "border-bottom-right-radius: 10px;"
            f"height: 62px; width: {SIDE_TAB_WIDTH}px;"
            "padding: 0px 0px 0px 0px;"  # top, right, bottom, left
            "margin: 0px 0px 3px 3px;}"  # top, right, bottom, left
            "color: black"
        )

        self.tabWidget_main.setStyleSheet(tabWidgetStyle)

        buttonStyle = (
            "QPushButton {border: 2px solid rgb(108, 204, 244);"
            "border-radius: 12px;"
            "padding: 0px 3px 0px 3px;"  # top, right, bottom, left
            "margin: 0px 0px 0px 0px;"  # top, right, bottom, left
            "text-align: center;"
            # "width: 130px;"
            # "border-top-left-radius: 10px;"
            # "border-bottom-right-radius: 10px;"
            f"height: {ITEM_HEIGHT}px;"
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
            f"height: {ITEM_HEIGHT}px;"
            "background-color: transparent;"
        )
        self.label_sendAddress.setStyleSheet(labelStyle)
        self.label_message.setStyleSheet(labelStyle)
        self.label_amount.setStyleSheet(labelStyle)
        self.label_accountName.setStyleSheet(labelStyle)
        self.label_sendValue.setStyleSheet(labelStyle)
        self.label_activeAddress.setStyleSheet(labelStyle)
        self.label_customizationArea.setStyleSheet(labelStyle)
        self.label_nodeProvider.setStyleSheet(labelStyle)
        self.label_amountVal.setStyleSheet(labelStyle)
        self.label_GasFeePriority.setStyleSheet(labelStyle)
        self.label_amountVal.setText(
            '<span style = "color: red; font-weight: bold;" > 0'
            '</ span> <span style = "color: rgb(140, 170, 250); font-weight: bold;" > ETH </ span>')
        lineEditStyle = (
            f"height: {ITEM_HEIGHT}px;"
            "background-color: rgb(250, 240, 200); color: black"
        )
        self.lineEdit_nodeProvider.setStyleSheet(lineEditStyle)
        self.lineEdit_sendAddress.setStyleSheet(lineEditStyle)
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
        comboBoxStyle = (
            "background-color: rgb(30, 76, 108); color: black; "
            "selection-background-color: rgb(47, 54, 60); selection-color: white; "
            "padding: 3px 3px 3px 3px;"  # top, right, bottom, left
            "margin: 0px 0px 0px 0px;"  # top, right, bottom, left
            # "text-align: center;"
        )
        self.comboBox_activeAddressVal.setStyleSheet(comboBoxStyle)
        self.comboBox_GasFeePriority.setStyleSheet(comboBoxStyle)

        self.textEdit_main.setStyleSheet("background-color: black; color: cyan")

        self.resetStatueBarStyleSheet()

    def resetStatueBarStyleSheet(self):
        self.statusbar.clearMessage()
        statusbarStyle = (
            "background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,"
            "stop:0 rgb(30, 76, 108) , stop:1 rgb(47, 54, 60)); color: white;"
        )
        self.statusbar.setStyleSheet(statusbarStyle)

    def setClickEvents(self):
        self.pushButton_copyAddress.clicked.connect(self.copyAddress)
        self.pushButton_etherScan.clicked.connect(self.goToEtherscan)
        self.pushButton_nodeProvider.clicked.connect(self.goToEtherNodes)
        self.pushButton_accountName.clicked.connect(self.editAccountName)
        self.pushButton_deleteAccount.clicked.connect(self.deleteAccount)
        self.pushButton_send.clicked.connect(self.send)
        # Wallets-New wallet---------------------------------------------------------------------------------
        self.action_newRandomAccount.triggered.connect(self.createAccountRandom)
        self.action_recoverFromMnemonic.triggered.connect(self.createAccountFromMnemonic)
        self.action_recoverFromEntropy.triggered.connect(self.createAccountFromEntropy)
        self.action_recoverFromPrivateKey.triggered.connect(self.createAccountFromPrivateKey)
        # Wallets-Secrets-------------------------------------------------------------------------------------
        self.action_entropy.triggered.connect(lambda: self.showSecrets(dataTypes.SECRET.ENTROPY))
        self.action_privateKey.triggered.connect(lambda: self.showSecrets(dataTypes.SECRET.PRIVATE_KEY))
        self.action_publicKeyCoordinates.triggered.connect(lambda: self.showSecrets(dataTypes.SECRET.PUBLIC_KEY_X))
        self.action_publicKey.triggered.connect(lambda: self.showSecrets(dataTypes.SECRET.PUBLIC_KEY))
        self.action_mnemonic.triggered.connect(lambda: self.showSecrets(dataTypes.SECRET.MNEMONIC))
        # NWallets-Backup&Restore------------------------------------------------------------------------------
        self.action_backup.triggered.connect(self.backupWallet)
        self.action_restore.triggered.connect(self.restoreWallet)
        # Network-Transactions---------------------------------------------------------------------------------
        self.action_checkTx.triggered.connect(self.showCustomTransaction)
        self.action_txNonce.triggered.connect(self.showNonce)
        self.action_simpleHistory.triggered.connect(self.showSimpleHistory)
        self.action_allNormal.triggered.connect(self.showNormalTransactions)
        self.action_allInternal.triggered.connect(self.showInternalTransactions)
        # Network-Tools-----------------------------------------------------------------------------------------
        self.action_publicKeyFromTxHash.triggered.connect(self.showSenderPublicKey)
        self.action_transactionMessage.triggered.connect(self.showCustomTransactionMessage)
        self.action_pendingTransactions.triggered.connect(self.showPendingTransactions)
        # -------------------------------------------------------------------------------------------------------
        self.radioButton_mainNet.toggled.connect(self.changeNetwork)
        self.radioButton_testNet.toggled.connect(self.changeNetwork)
        # -------------------------------------------------------------------------------------------------------
        self.lineEdit_sendValue.textChanged.connect(self.lineEditSendValueChange)
        self.comboBox_activeAddressVal.currentTextChanged.connect(self.comboBoxChange)

    def setMenuActionsTips(self):
        # Wallets-New wallet-------------------------------------------------------------------------------------
        self.action_newRandomAccount.setShortcut('Ctrl+n')
        self.action_newRandomAccount.setStatusTip('create new random account')
        self.action_recoverFromMnemonic.setShortcut('Ctrl+m')
        self.action_recoverFromMnemonic.setStatusTip('recover an old account from mnemonic')
        self.action_recoverFromEntropy.setShortcut('Ctrl+e')
        self.action_recoverFromEntropy.setStatusTip('recover an old account from entropy')
        self.action_recoverFromPrivateKey.setShortcut('Ctrl+p')
        self.action_recoverFromPrivateKey.setStatusTip('recover an old account from the private Key')
        # Wallets-Secrets---------------------------------------------------------------------------------
        self.action_entropy.setShortcut('Alt+e')
        self.action_entropy.setStatusTip('see your account entropy')
        self.action_privateKey.setShortcut('Alt+p')
        self.action_privateKey.setStatusTip('see your account private key')
        # self.action_publicKeyCoordinates.setShortcut('Alt+p+c')
        self.action_publicKeyCoordinates.setStatusTip('see your account public Key Coordinates')
        self.action_publicKey.setShortcut('Alt+k')
        self.action_publicKey.setStatusTip('see your account public Key')
        self.action_mnemonic.setShortcut('Alt+m')
        self.action_mnemonic.setStatusTip('see your account mnemonic words')
        # Wallets-Backup&Restore------------------------------------------------------------------------------
        self.action_backup.setShortcut('Ctrl+b')
        self.action_backup.setStatusTip('back up your account to file')
        self.action_restore.setShortcut('Ctrl+r')
        self.action_restore.setStatusTip('restore your account from file')
        # Network-Transactions---------------------------------------------------------------------------------
        self.action_checkTx.setShortcut('Alt+t')
        self.action_checkTx.setStatusTip('view a transaction details')
        self.action_txNonce.setShortcut('Alt+n')
        self.action_txNonce.setStatusTip('view sent transaction count')
        self.action_simpleHistory.setShortcut('Alt+h')
        self.action_simpleHistory.setStatusTip('simple history of your account transactions. up to last 10000 block')
        # self.action_allNormal.setShortcut('Alt+n+t')
        self.action_allNormal.setStatusTip('simple history of your normal transactions. up to last 10000 block')
        # self.action_allInternal.setShortcut('Alt+i+t')
        self.action_allInternal.setStatusTip('simple history of your internal transactions. up to last 10000 block')
        # Network-Tools-----------------------------------------------------------------------------------------
        # self.action_publicKeyFromTxHash.setShortcut('Alt+m')
        self.action_publicKeyFromTxHash.setStatusTip('recover sender public key from transaction hash')
        # self.action_transactionMessage.setShortcut('Alt+m')
        self.action_transactionMessage.setStatusTip('view the embedded message in a transaction')
        # self.action_pendingTransactions.setShortcut('Alt+p')
        self.action_pendingTransactions.setStatusTip('view non-verified transactions')

    def changeNetwork(self):
        try:
            if self.radioButton_mainNet.isChecked() and not self.radioButton_testNet.isChecked():
                self.lineEdit_nodeProvider.setText(ETHEREUM_PROVIDER)
            elif not self.radioButton_mainNet.isChecked() and self.radioButton_testNet.isChecked():
                self.lineEdit_nodeProvider.setText(SEPOLIA_PROVIDER)
            else:
                raise Exception("unknown network status")
        except Exception as er:
            gui_error.WINDOW('changeNetwork', str(er)).exec()

    def comboBoxChange(self):
        try:
            if self.comboBox_activeAddressVal.count() == 0:
                self.lineEdit_accountName.clear()
                self.label_amountVal.setText(
                    '<span style = "color: red; font-weight: bold;" > 0 '
                    '</ span> <span style = "color: rgb(140, 170, 250); font-weight: bold;" > ETH </ span>')
            else:
                name = self.db.readColumn('NAM', self.comboBox_activeAddressVal.currentText())[0][0]
                self.lineEdit_accountName.setText(name)
        except Exception as er:
            gui_error.WINDOW("comboBoxChange", str(er)).exec()

    def editAccountName(self):
        try:
            if self.pushButton_accountName.text() == 'Edit':
                self.lineEdit_accountName.setEnabled(True)
                self.lineEdit_accountName.setStyleSheet("background-color: rgb(250, 240, 200); color: black")
                self.pushButton_accountName.setText('Save')
                self.pushButton_accountName.setIcon(QtGui.QIcon(system.getIconPath('save.png')))
                self.pushButton_nodeProvider.setIconSize(QSize(ICON_SIZE, ICON_SIZE))
            elif self.pushButton_accountName.text() == 'Save':
                self.lineEdit_accountName.setEnabled(False)
                self.lineEdit_accountName.setStyleSheet(
                    "background-color: transparent; border: none;"
                    "color: rgb(108, 204, 244); font-weight: bold;")
                self.pushButton_accountName.setText('Edit')
                self.pushButton_accountName.setIcon(QtGui.QIcon(system.getIconPath('edit.png')))
                self.pushButton_nodeProvider.setIconSize(QSize(ICON_SIZE, ICON_SIZE))
                self.db.updateRowValue('NAM', self.lineEdit_accountName.text(),
                                       self.comboBox_activeAddressVal.currentText())
        except Exception as er:
            gui_error.WINDOW('editAccountName', str(er)).exec()

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
            print(str(er))
            pass  # nothing to do

    def createAccountRandom(self):
        try:
            userAnswer = True
            if self.db.isAccountExist():
                createAccount_window = gui_userChoice.WINDOW('Create new random account',
                                                             'Some account(s) already exist',
                                                             'Create new one?')
                createAccount_window.exec()
                userAnswer = createAccount_window.getAnswer()
            else:
                pass  # it is first account continue to create one
            if not userAnswer:
                pass  # cancel by user or it is new account
            else:
                acc = account.New.random()  # create new account
                acc['name'] = 'No name'
                self.db.insertRow(acc)
                self.comboBox_activeAddressVal.addItem(acc['address'])
                self.comboBox_activeAddressVal.setCurrentIndex(self.comboBox_activeAddressVal.count() - 1)
        except Exception as er:
            gui_error.WINDOW('createAccountRandom', str(er)).exec()

    def createAccountFromEntropy(self):
        try:
            getEntropy = gui_userInput.WINDOW('Recover account from entropy',
                                              'Enter your entropy:')
            getEntropy.exec()
            entropy = getEntropy.getInput()
            if entropy == '':
                gui_message.WINDOW('Recover account from entropy', 'Nothing received',
                                   'you can try again from Wallet -> New account -> Recover from entropy').exec()
            else:
                acc = account.New.fromEntropy(entropy)
                acc['name'] = 'No name'
                self.db.insertRow(acc)
                self.comboBox_activeAddressVal.addItem(acc['address'])
                self.comboBox_activeAddressVal.setCurrentIndex(self.comboBox_activeAddressVal.count() - 1)
        except Exception as er:
            gui_error.WINDOW('createAccountFromEntropy', str(er)).exec()

    def createAccountFromPrivateKey(self):
        try:
            getPrivateKey = gui_userInput.WINDOW('Recover account from privateKey',
                                                 'Enter your private key:')
            getPrivateKey.exec()
            privateKey = getPrivateKey.getInput()
            if privateKey == '':
                gui_message.WINDOW('Recover account from privateKey', 'Nothing received',
                                   'you can try again from Wallet -> New account -> Recover from private key').exec()
            else:
                acc = account.New.fromPrivateKey(privateKey)
                acc['name'] = 'No name'
                self.db.insertRow(acc)
                self.comboBox_activeAddressVal.addItem(acc['address'])
                self.comboBox_activeAddressVal.setCurrentIndex(self.comboBox_activeAddressVal.count() - 1)
        except Exception as er:
            gui_error.WINDOW('createAccountFromPrivateKey', str(er)).exec()

    def createAccountFromMnemonic(self):
        try:
            getMnemonic = gui_userInput.WINDOW('Recover account from mnemonic', 'Enter your mnemonic:')
            getMnemonic.exec()
            mnemonic = getMnemonic.getInput()
            if mnemonic == '':
                gui_message.WINDOW('Recover account from mnemonic', 'Nothing received',
                                   'you can try again from Wallet -> New account -> Recover from mnemonic').exec()
            else:
                acc = account.New.fromMnemonic(mnemonic)
                acc['name'] = 'No name'
                self.db.insertRow(acc)
                self.comboBox_activeAddressVal.addItem(acc['address'])
                self.comboBox_activeAddressVal.setCurrentIndex(self.comboBox_activeAddressVal.count() - 1)
        except Exception as er:
            gui_error.WINDOW('createAccountFromMnemonic', str(er)).exec()

    def goToEtherscan(self):
        try:
            active_address = self.comboBox_activeAddressVal.currentText()
            if active_address is None:
                gui_message.WINDOW('goToEtherscan', 'No address selected').exec()
            else:
                if self.radioButton_mainNet.isChecked() and not self.radioButton_testNet.isChecked():
                    self.webEngineView.setUrl(QUrl(f"https://etherscan.io/address/{active_address}"))
                    self.tabWidget_main.setCurrentIndex(4)
                elif not self.radioButton_mainNet.isChecked() and self.radioButton_testNet.isChecked():
                    self.webEngineView.setUrl(QUrl(f"https://sepolia.etherscan.io/address/{active_address}"))
                    self.tabWidget_main.setCurrentIndex(4)
                else:
                    raise Exception("unknown network status")
        except Exception as er:
            gui_error.WINDOW('goToEtherscan', str(er)).exec()

    def goToEtherNodes(self):
        try:
            if self.radioButton_mainNet.isChecked() and not self.radioButton_testNet.isChecked():
                self.webEngineView.setUrl(QUrl(f"https://ethereumnodes.com/"))
                self.tabWidget_main.setCurrentIndex(4)
            elif not self.radioButton_mainNet.isChecked() and self.radioButton_testNet.isChecked():
                self.webEngineView.setUrl(QUrl(f"https://sepolia.dev/"))
                self.tabWidget_main.setCurrentIndex(4)
            else:
                raise Exception("unknown network status")
        except Exception as er:
            gui_error.WINDOW('goToEtherNodes', str(er)).exec()

    def copyAddress(self):
        try:
            active_address = self.comboBox_activeAddressVal.currentText()
            if active_address is not None:
                copy(active_address)
            # spam = pyperclip.paste()
        except Exception as er:
            gui_error.WINDOW('copyAddress', str(er)).exec()

    def showSecrets(self, secretType: dataTypes.SECRET):
        try:
            self.textEdit_main.clear()
            if secretType == dataTypes.SECRET.ENTROPY and (self.db.readColumn(
                    dataTypes.SECRET.ENTROPY.value, self.comboBox_activeAddressVal.currentText()
            ) == self.db.readColumn(dataTypes.SECRET.PRIVATE_KEY.value,
                                    self.comboBox_activeAddressVal.currentText())):
                gui_message.WINDOW('Show secrets',
                                   'You have recovered an old account.',
                                   'Entropy is not recoverable from private key').exec()
            elif secretType == dataTypes.SECRET.MNEMONIC and (self.db.readColumn(
                    dataTypes.SECRET.MNEMONIC.value, self.comboBox_activeAddressVal.currentText()
            ) == self.db.readColumn(dataTypes.SECRET.PRIVATE_KEY.value,
                                    self.comboBox_activeAddressVal.currentText())):
                gui_message.WINDOW('Show secrets',
                                   'You have recovered an old account.',
                                   'Mnemonic is not recoverable from private key').exec()
            elif secretType == dataTypes.SECRET.PUBLIC_KEY_X or secretType == dataTypes.SECRET.PUBLIC_KEY_Y:
                result_X = self.db.readColumn(
                    dataTypes.SECRET.PUBLIC_KEY_X.value, self.comboBox_activeAddressVal.currentText())
                result_Y = self.db.readColumn(
                    dataTypes.SECRET.PUBLIC_KEY_Y.value, self.comboBox_activeAddressVal.currentText())
                if len(result_X) == 1 and len(result_Y) == 1:
                    self.textEdit_main.append(f'Your account PUBLIC_KEY COORDINATE keep it safe:\n')
                    self.textEdit_main.append('X : ' + result_X[0][0])
                    self.textEdit_main.append('Y : ' + result_Y[0][0])
                else:
                    raise Exception(f"failed to receive coordinates from database.\nX: {result_X}\nY: {result_Y}")
            else:
                result = self.db.readColumn(secretType.value, self.comboBox_activeAddressVal.currentText())
                if len(result) == 1:
                    self.textEdit_main.append(f'Your account {secretType.name} keep it safe:\n')
                    self.textEdit_main.append(f'{result[0][0]}\n')
                    if secretType == dataTypes.SECRET.MNEMONIC or secretType == dataTypes.SECRET.ENTROPY:
                        self.textEdit_main.append(f'{secretType.name} + Passphrase = your account\n\n'
                                                  f'{secretType.name} without Passphrase = unknown account\n'
                                                  f'(If no passphrase set = your account)')
                    elif secretType == dataTypes.SECRET.PRIVATE_KEY:
                        self.textEdit_main.append(f'{secretType.name} = your account')
                else:
                    raise Exception(f"failed to receive {secretType.name} from database.")
        except Exception as er:
            gui_error.WINDOW('showSecrets', str(er)).exec()

    def getBalance(self):
        try:
            if not self.comboBox_activeAddressVal.count() == 0:  # 0 means no account available
                checkURL(self.lineEdit_nodeProvider.text())
                balance = ethereum.getBalance(self.comboBox_activeAddressVal.currentText(),
                                              self.lineEdit_nodeProvider.text())
                if balance < 0:
                    # error in getting balance
                    self.statusbar.showMessage(f"negative balance ! something is wrong")
                else:
                    color = 'red'
                    if balance > 0:
                        color = 'green'
                    self.label_amountVal.setText(
                        '<span style = "color: ' + color + '; font-weight: bold;" > ' + str(balance) +
                        '</ span> <span style = "color: rgb(140, 170, 250); font-weight: bold;" > ETH </ span>')
                    self.resetStatueBarStyleSheet()
                    print('balance = ', balance)
        except Exception as er:
            self.statusbar.setStyleSheet("background-color: red; color: white")
            self.statusbar.showMessage(f"balance is not synchronized. {er}")

    def transactionElements(self, data: str = ''):
        try:
            if self.radioButton_mainNet.isChecked() and not self.radioButton_testNet.isChecked():
                chainId = 1  # Ethereum chain ID
            elif not self.radioButton_mainNet.isChecked() and self.radioButton_testNet.isChecked():
                chainId = 11155111  # Sepolia chain ID
            else:
                raise Exception("unknown network status")

            if chainId == 1 or chainId == 11155111:
                if not self.lineEdit_sendValue.text():
                    val = 0  # just message no ETH value
                else:
                    val = float(self.lineEdit_sendValue.text())

                if not self.lineEdit_sendAddress.text():
                    to = ''  # for contracts
                else:
                    to = self.lineEdit_sendAddress.text()
                checkURL(self.lineEdit_nodeProvider.text())
                print('chainId = ', chainId)
                return {
                    'sender': self.comboBox_activeAddressVal.currentText(),
                    'receiver': to,
                    'vale': val,
                    'provider': self.lineEdit_nodeProvider.text(),
                    'chainId': chainId,
                    'data': data
                }
            else:
                raise Exception("selecting main or test net")
        except Exception as er:
            gui_error.WINDOW('transactionElements', str(er)).exec()

    def showPendingTransactions(self):
        pendingBlock = ethereum.getPendingTransactions(self.lineEdit_nodeProvider.text())
        print()

    def send(self, duplicate: bool = False):
        try:
            if self.lineEdit_message.text():
                self.sentMessage(duplicate)
            elif not self.lineEdit_message.text() and self.lineEdit_sendValue.text():
                self.sentETH(duplicate)
            elif not self.lineEdit_message.text() and not self.lineEdit_sendValue.text():
                raise Exception(f"sending options are empty")
            else:
                raise Exception(f"send parameters!")
            print(self.transactionResult)
            if self.transactionResult['message'] == 'succeed':
                gui_message.WINDOW("Your job is done', 'Transaction succeed:",
                                   f"Hash: {self.transactionResult['hash']}").exec()
                self.showTransaction(self.transactionResult['hash'])
                cursor = QTextCursor(self.textEdit_main.document())
                cursor.setPosition(0)
                self.textEdit_main.setTextCursor(cursor)
                self.textEdit_main.insertPlainText(f"transaction Hash:\n{self.transactionResult['hash']}\n"
                                                   f"--------------------\n")
                self.lineEdit_sendValue.clear()
                self.lineEdit_message.clear()
                self.lineEdit_sendAddress.clear()
        except Exception as er:
            gui_error.WINDOW('send', str(er)).exec()
            if self.transactionResult['message'] == 'replacement transaction underpriced':
                nonceWindow = gui_userChoice.WINDOW('send',
                                                    f"{self.transactionResult['pending']} transaction(s) "
                                                    f"also waiting for confirmation.\n"
                                                    f"you can change transaction nonce and force it to submit.",
                                                    f"(if you see this message repeatedly, "
                                                    f"cancel this dialog and wait for pending transaction fate)\n"
                                                    f"want to do it or cancel it?")
                nonceWindow.exec()
                userAnswer = nonceWindow.getAnswer()
                if not userAnswer:
                    pass
                else:
                    self.send(True)

    def setPriority(self, transactions, gas) -> dict:
        try:
            if self.comboBox_GasFeePriority.currentIndex() == 0:
                transactions['maxFeePerGas'] = gas['MAX_Fee']['high']
                transactions['MAXPriorityFee'] = gas['MAXPriorityFee']['high']
                transactions['GasPrice'] = gas['GasPrice']['high']
            elif self.comboBox_GasFeePriority.currentIndex() == 1:
                transactions['maxFeePerGas'] = gas['MAX_Fee']['medium']
                transactions['MAXPriorityFee'] = gas['MAXPriorityFee']['medium']
                transactions['GasPrice'] = gas['GasPrice']['medium']
            elif self.comboBox_GasFeePriority.currentIndex() == 2:
                transactions['maxFeePerGas'] = gas['MAX_Fee']['low']
                transactions['MAXPriorityFee'] = gas['MAXPriorityFee']['low']
                transactions['GasPrice'] = gas['GasPrice']['low']
            else:
                raise Exception(f"unknown priority")
            return transactions
        except Exception as er:
            raise Exception(f"setPriority -> {er}")

    def sentETH(self, duplicate: bool = False):
        try:
            if not self.lineEdit_sendAddress.text():
                raise Exception(f"address = '{self.lineEdit_sendAddress.text()}' !")

            if not self.lineEdit_sendValue.text():
                raise Exception(f"value = '{self.lineEdit_sendValue.text()}' !")

            transactions = self.transactionElements()
            gas = ethereum.estimateGas(transactions)
            senETH = gui_userChoice.WINDOW('Sending your money to others',
                                           f"Send: {transactions['vale']} ETH\n"
                                           f"to: '{transactions['receiver']}'\n"
                                           f"estimated gas fee is:\n"
                                           f"Lowest: {gas['GasPrice']['low']} ETH\n"
                                           f"Median: {gas['GasPrice']['medium']} ETH\n"
                                           f"Highest: {gas['GasPrice']['high']} ETH\n",
                                           'Are you sure?')
            senETH.exec()
            if not senETH.getAnswer():  # cancel by user
                gui_message.WINDOW('I\'m entranced with joy', 'You are in safe',
                                   'Nothing has been sent').exec()
            else:
                transactions = self.setPriority(transactions, gas)
                transactionResult = ethereum.sendValueTransaction(privateKey=(self.db.readColumn(
                    dataTypes.SECRET.PRIVATE_KEY.value, transactions['sender']))[0][0],
                                                                  txElements=transactions,
                                                                  duplicate=duplicate)
                self.transactionResult = transactionResult
                if self.transactionResult['message'] != 'succeed':
                    raise Exception(f"{self.transactionResult['message']}")
        except Exception as er:
            raise Exception(f"sentETH -> {er}")

    def sentMessage(self, duplicate: bool = False):
        try:
            if not self.lineEdit_sendAddress.text():
                raise Exception(f"address = '{self.lineEdit_sendAddress.text()}' !")

            if not self.lineEdit_message.text():
                raise Exception(f"message = '{self.lineEdit_sendValue.text()}' !")
            message = self.lineEdit_message.text()

            transactions = self.transactionElements(data=message.encode("utf-8").hex())
            gas = ethereum.estimateGas(transactions)
            senMSG = gui_userChoice.WINDOW("Sending your message to others",
                                           f"Send message: '{message}'\n"
                                           f"and value: '{transactions['vale']}' ETH\n"
                                           f"to {transactions['receiver']}\n"
                                           f"\nestimated gas fee is:\n"
                                           f"Lowest = {gas['GasPrice']['low']} ETH\n"
                                           f"Median = {gas['GasPrice']['medium']} ETH\n"
                                           f"Highest = {gas['GasPrice']['high']} ETH\n",
                                           'Are you sure?')
            senMSG.exec()
            if not senMSG.getAnswer():  # cancel by user
                gui_message.WINDOW('I\'m entranced with joy', 'You are in safe',
                                   'Nothing has been sent').exec()
            else:
                transactions = self.setPriority(transactions, gas)
                transactionResult = ethereum.sendMessageTransaction(privateKey=(self.db.readColumn(
                    dataTypes.SECRET.PRIVATE_KEY.value, transactions['sender']))[0][0],
                                                                    txElements=transactions,
                                                                    duplicate=duplicate)
                self.transactionResult = transactionResult
                if self.transactionResult['message'] != 'succeed':
                    raise Exception(f"{self.transactionResult['message']}")
        except Exception as er:
            raise Exception(f"sentMessage -> {er}")

    def showTransaction(self, txHash):
        try:
            checkURL(self.lineEdit_nodeProvider.text())
            checkHex(txHash)
            tx = ethereum.getTransaction(txHash, self.lineEdit_nodeProvider.text())
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
            raise Exception('showTransaction -> ', str(er))

    def showTransactionMessage(self, txHash):
        try:
            checkURL(self.lineEdit_nodeProvider.text())
            checkHex(txHash)
            tx = ethereum.getTransaction(txHash, self.lineEdit_nodeProvider.text())
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
            gui_error.WINDOW('showTransactionMessage', str(er)).exec()

    def showCustomTransaction(self):
        try:
            TXHashWindow = gui_userInput.WINDOW('Show custom transaction',
                                                'Enter transaction hash:\n'
                                                '(Notice about mainNet and testNet)')
            TXHashWindow.exec()
            TXHash = TXHashWindow.getInput()
            if TXHash:
                checkHex(TXHash)
                self.showTransaction(TXHash)
        except Exception as er:
            gui_error.WINDOW('showCustomTransaction', str(er)).exec()

    def showCustomTransactionMessage(self):
        try:
            TXHashWindow = gui_userInput.WINDOW('Show custom transaction message',
                                                'Enter transaction hash:\n'
                                                '(Notice about mainNet and testNet)')
            TXHashWindow.exec()
            TXHash = TXHashWindow.getInput()
            if TXHash:
                checkHex(TXHash)
                self.showTransactionMessage(TXHash)
        except Exception as er:
            gui_error.WINDOW('showCustomTransactionMessage', str(er)).exec()

    def showNonce(self):
        try:
            checkURL(self.lineEdit_nodeProvider.text())
            nonce = ethereum.getAccountNonce(self.comboBox_activeAddressVal.currentText(),
                                             self.lineEdit_nodeProvider.text())
            self.textEdit_main.clear()
            self.textEdit_main.append(f'Your current sent transaction count is {nonce}')
        except Exception as er:
            gui_error.WINDOW('showNonce', str(er)).exec()

    def getTransactions(self, APIkey: str, isInternal: bool) -> list:
        try:
            if self.radioButton_mainNet.isChecked() and not self.radioButton_testNet.isChecked():
                mainNet = True
            elif not self.radioButton_mainNet.isChecked() and self.radioButton_testNet.isChecked():
                mainNet = False
            else:
                raise Exception("unknown network status")

            if not self.comboBox_activeAddressVal.currentText():
                raise Exception(f"address = '{self.comboBox_activeAddressVal.currentText()}' !")
            checkURL(self.lineEdit_nodeProvider.text())
            if not self.lineEdit_nodeProvider.text():
                raise Exception(f"provider = '{self.lineEdit_nodeProvider.text()}' !")
            if isInternal:
                txHistory = ethereum.getTransactionHistory(self.comboBox_activeAddressVal.currentText(),
                                                           self.lineEdit_nodeProvider.text(), APIkey, mainNet,
                                                           isInternal)
            else:
                txHistory = ethereum.getTransactionHistory(self.comboBox_activeAddressVal.currentText(),
                                                           self.lineEdit_nodeProvider.text(), APIkey, mainNet,
                                                           isInternal)
            txHistory = loads(txHistory.decode('utf-8'))
            if not txHistory['status'] == '1' or not txHistory['message'] == 'OK':
                raise Exception(f"bad response\n.{txHistory}")
            else:
                return txHistory['result']
        except Exception as er:
            raise Exception('getTransactions -> ', str(er))

    def showSimpleHistory(self):
        try:
            TXHistoryWindow = gui_userInput.WINDOW('Show simple history', 'Enter your APIkey:\n'
                                                                          '(Notice about mainNet and testNet)')
            TXHistoryWindow.exec()
            APIkey = TXHistoryWindow.getInput()
            if APIkey:
                txHistoryNormal = self.getTransactions(APIkey, False)
                txHistoryInternal = self.getTransactions(APIkey, True)

                if len(txHistoryNormal) > 0 or len(txHistoryInternal) > 0:  # there is something for show
                    if len(txHistoryNormal) <= 0:
                        gui_message.WINDOW("showSimpleHistory", "there is no normal transaction")

                    if len(txHistoryInternal) <= 0:
                        gui_message.WINDOW("showSimpleHistory", "there is no internal transaction")

                    allTransactions = txHistoryNormal + txHistoryInternal
                    #  sort ace
                    sortedTransactions = sorted(allTransactions, key=lambda d: d['blockNumber'])
                    # de sort
                    sortedTransactions = sortedTransactions[::-1]
                    self.textEdit_main.clear()
                    self.textEdit_main.append(f'Total {len(sortedTransactions)} transaction(s) received:\n'
                                              f'Offset is last 10000')
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
                    raise Exception(f"account data has not been received")
        except Exception as er:
            gui_error.WINDOW('showSimpleHistory', str(er)).exec()

    def showNormalTransactions(self):
        try:
            TXHistoryWindow = gui_userInput.WINDOW('Show normal transactions', 'Enter your APIkey:\n'
                                                                               '(Notice about mainNet and testNet)')
            TXHistoryWindow.exec()
            APIkey = TXHistoryWindow.getInput()
            if APIkey:
                txHistory = self.getTransactions(APIkey, False)
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
            gui_error.WINDOW('showNormalTransactions', str(er)).exec()

    def showInternalTransactions(self):
        try:
            TXHistoryWindow = gui_userInput.WINDOW('Show internal transactions', 'Enter your APIkey:\n'
                                                                                 '(Notice about mainNet and testNet)')
            TXHistoryWindow.exec()
            APIkey = TXHistoryWindow.getInput()
            if APIkey:
                txHistory = self.getTransactions(APIkey, True)
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
            gui_error.WINDOW('showInternalTransactions', str(er)).exec()

    def showSenderPublicKey(self):
        try:
            TxHashWindow = gui_userInput.WINDOW('Show sender publicKey', 'Enter transaction hash:\n'
                                                                         '(You will get sender publicKey and address)')
            TxHashWindow.exec()
            TxHash = TxHashWindow.getInput()
            if TxHash:
                checkHex(TxHash)
                checkURL(self.lineEdit_nodeProvider.text())
                result = ethereum.getPublicKeyFromTransaction(TxHash, self.lineEdit_nodeProvider.text())
                self.textEdit_main.clear()
                self.textEdit_main.append(f"\nSender address: {result['address']}\n"
                                          f"Sender publicKey: {result['publicKey']}")
                cursor = QTextCursor(self.textEdit_main.document())
                cursor.setPosition(0)
                self.textEdit_main.setTextCursor(cursor)
        except Exception as er:
            gui_error.WINDOW('showSenderPublicKey', str(er)).exec()

    def backupWallet(self):
        try:
            if not self.comboBox_activeAddressVal.currentText():
                raise Exception(f"address = '{self.comboBox_activeAddressVal.currentText()}' !")
            rowData = self.db.readRow(self.comboBox_activeAddressVal.currentText())[0]
            data = {'entropy': rowData[0],
                    'privateKey': rowData[1],
                    'publicKeyCoordinate': (rowData[2], rowData[3]),
                    'publicKey': rowData[4],
                    'address': rowData[5],
                    'mnemonic': rowData[6],
                    'name': rowData[7]}
            root = Tk()
            root.withdraw()
            folderSelected = filedialog.askdirectory()
            fileName = ''
            dataToWrite = None
            if folderSelected:
                passwordWindow = gui_userInput.WINDOW('backupWallet',
                                                      'Exporting the secrets of your account to the file.\n'
                                                      'For more security set a password on the file\n'
                                                      'or cancel for skip password protection')
                passwordWindow.exec()
                password = passwordWindow.getInput()
                if password:
                    fileName = f"{folderSelected}/{rowData[7].replace(' ', '_')}.wallet"
                    b_password = password.encode('utf-8')
                    b_data = dumps(data, indent=2).encode('utf-8')
                    dataToWrite = DES.encrypt(b_password, b_data)
                else:
                    fileName = f"{folderSelected}/{rowData[7].replace(' ', '_')}.json"
                    dataToWrite = data

                if Path(fileName).is_file():
                    reWriteWindow = gui_userChoice.WINDOW('backupWallet', 'File is exist!',
                                                          'Overwrite it?')

                    reWriteWindow.exec()
                    WriteOnFile = reWriteWindow.getAnswer()
                else:
                    WriteOnFile = True
                if WriteOnFile:
                    with open(fileName, 'w+') as fp:
                        dump(dataToWrite, fp)
                    if Path(fileName).is_file():
                        gui_message.WINDOW('backupWallet', f"'{fileName}'\nsuccessfully saved.").exec()
                    else:
                        raise Exception('saving file failed.')
                else:
                    pass  # cancel by user
            if not fileName or dataToWrite is None:
                raise Exception(f"error...\nfile name: '{fileName}'\ndata: '{dataToWrite}'")
        except Exception as er:
            gui_error.WINDOW('backupWallet', str(er)).exec()

    def restoreWallet(self):
        try:
            root = Tk()
            root.withdraw()
            filePath = filedialog.askopenfilename()
            if not filePath:
                pass  # cancel by user
            else:
                with open(filePath, 'r') as f:  # open the file
                    data = f.readlines()[0]
                if filePath.endswith('.json'):  # non encrypted file
                    jsonData = loads(data)
                elif filePath.endswith('.wallet'):  # an encrypted file
                    passwordWindow = gui_userInput.WINDOW('restoreWallet', 'This is an encrypted file.\n'
                                                                           "Enter the file password:\n")
                    passwordWindow.exec()
                    password = passwordWindow.getInput()
                    if not password:  # no password received
                        raise Exception(f"restoring encrypted account need password")
                    else:
                        decrypted = DES.decrypt(password.encode('utf-8'), data)
                        jsonData = loads(decrypted.decode('utf-8'))
                else:
                    raise Exception(f"unknown file format")
                self.showWallet(jsonData, filePath)
                self.db.insertRow(jsonData)
                self.comboBox_activeAddressVal.addItem(jsonData['address'])
                self.comboBox_activeAddressVal.setCurrentIndex(self.comboBox_activeAddressVal.count() - 1)
        except Exception as er:
            gui_error.WINDOW('restoreWallet', str(er)).exec()

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
            gui_error.WINDOW('showWallet', str(er)).exec()

    def deleteAccount(self):
        try:
            accountToDelete = self.comboBox_activeAddressVal.currentText()
            if not accountToDelete:
                raise Exception(f"address = '{accountToDelete}' !")
            accountIndex = self.comboBox_activeAddressVal.currentIndex()
            accountName = self.lineEdit_accountName.text()
            deleteWindow = gui_userChoice.WINDOW('deleteAccount',
                                                 f'Delete account \"{accountName}\"?\n'
                                                 f'account address: {accountToDelete}\n',
                                                 'You will lost that\n'
                                                 'Proceed?')
            deleteWindow.exec()
            deleteIt = deleteWindow.getAnswer()
            if not deleteIt:
                gui_message.WINDOW('deleteAccount', 'Nothing has been removed.').exec()
            else:
                self.db.deleteRow(accountToDelete)
                if self.comboBox_activeAddressVal.count() == 1:
                    self.comboBox_activeAddressVal.clear()
                else:
                    self.comboBox_activeAddressVal.removeItem(accountIndex)
                self.textEdit_main.clear()
                gui_message.WINDOW('deleteAccount', 'the account was deleted.').exec()
        except Exception as er:
            gui_error.WINDOW('deleteAccount', str(er)).exec()
