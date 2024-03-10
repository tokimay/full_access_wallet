
from webbrowser import open
from pyperclip import copy
from PyQt6.QtWidgets import (QFrame, QWidget, QGridLayout, QLabel, QPushButton, QComboBox, QLineEdit,
                             QRadioButton, QTextEdit, QMenuBar, QMenu, QStatusBar)
from json import loads
from PyQt6 import QtWidgets
from PyQt6.QtCore import QSize, QRect
from PyQt6.QtGui import QIcon, QPixmap, QAction, QTextCursor
from src import (database, dataTypes, gui_errorDialog, qui_getUserChoice, qui_getUserInput, qui_showMessage, ethereum,
                 account, system)




class Ui(QtWidgets.QMainWindow):
    def __init__(self, dbName):
        super().__init__()
        self.menubar_file = QMenuBar(self)

        self.menu_Wallet = QMenu(self.menubar_file)
        self.menuSecrets = QMenu(self.menu_Wallet)
        self.menuNew_account = QMenu(self.menu_Wallet)

        self.menuNetwork = QMenu(self.menubar_file)
        self.menuTransactions = QMenu(self.menuNetwork)
        self.menuTools = QMenu(self.menuNetwork)

        self.setMenuBar(self.menubar_file)
        # ----------------------------------------------------------------------------------
        self.actionEntropy = QAction(self)
        self.actionPrivateKey = QAction(self)
        self.actionPublicKey_coordinates = QAction(self)
        self.actionPublicKey = QAction(self)
        self.actionMnemonic = QAction(self)
        # ----------------------------------------------------------------------------------
        self.actionNew_random_account = QAction(self)
        self.actionRecover_from_mnemonic = QAction(self)
        self.actionRecover_from_entropy = QAction(self)
        self.actionRecover_from_privateKey = QAction(self)
        # ----------------------------------------------------------------------------------
        self.action_checkTX = QAction(self)
        self.actionTX_nonce = QAction(self)
        self.actionSimple_history = QAction(self)
        self.actionAll_normal = QAction(self)
        self.actionAll_internal = QAction(self)
        # ----------------------------------------------------------------------------------
        self.actionPublicKey_from_TXHash = QAction(self)
        self.actionTransactionMessage = QAction(self)
        # ----------------------------------------------------------------------------------
        self.centralWidget = QWidget(self)
        self.gridLayoutWidget = QWidget(self.centralWidget)
        self.gridlayout = QGridLayout(self.gridLayoutWidget)
        # ----------------------------------------------------------------------------------
        # row 1
        self.label_node_provider = QLabel(self.gridLayoutWidget)
        self.lineEdit_node_provider = QLineEdit(self.gridLayoutWidget)
        self.pushButton_node_provider = QPushButton(self.gridLayoutWidget)

        # row 2
        self.label_accountName = QLabel(self.gridLayoutWidget)
        self.lineEdit_accountName = QLineEdit(self.gridLayoutWidget)
        self.pushButton_accountName = QPushButton(self.gridLayoutWidget)

        # row 3
        self.label_activeAddress = QLabel(self.gridLayoutWidget)
        self.comboBox_activeAddress_val = QComboBox(self.gridLayoutWidget)
        self.pushButton_copy_address = QPushButton(self.gridLayoutWidget)

        # row 4
        self.label_amount = QLabel(self.gridLayoutWidget)
        self.label_amount_val = QLabel(self.gridLayoutWidget)
        self.pushButton_ETH = QPushButton(self.gridLayoutWidget)

        # row 5
        self.label_send = QLabel(self.gridLayoutWidget)
        self.lineEdit_send = QLineEdit(self.gridLayoutWidget)

        # row 6
        self.label_sendValue = QLabel(self.gridLayoutWidget)
        self.lineEdit_sendValue = QLineEdit(self.gridLayoutWidget)
        self.pushButton_send = QPushButton(self.gridLayoutWidget)
        self.label_message = QLabel(self.gridLayoutWidget)
        self.LineEdit_message = QLineEdit(self.gridLayoutWidget)

        # row 7
        self.textEdit_main = QTextEdit(self.gridLayoutWidget)

        # customization
        self.label_customizationArea = QLabel(self.gridLayoutWidget)
        self.radioButton_mainNet = QRadioButton(self.gridLayoutWidget)
        self.radioButton_testNet = QRadioButton(self.gridLayoutWidget)

        self.line_vertical = QFrame(self.gridLayoutWidget)
        # ----------------------------------------------------------------------------------
        self.statusbar = QStatusBar(self)

        self.db = database.Sqlite(dbName)
        self.initUI()

    def initUI(self):
        self.setObjectName("MainWindow")
        self.setWindowTitle("FAwallet")
        self.resize(800, 600)

        self.setCentralWidget(self.centralWidget)
        self.centralWidget.setObjectName("centralWidget")
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayoutWidget.setGeometry(QRect(10, 10, 780, 580))
        self.gridlayout.setObjectName("gridlayout")
        self.gridlayout.setGeometry(QRect(10, 10, 780, 580))
        self.gridlayout.setContentsMargins(0, 0, 0, 0)
        # ----------------------------------------------------------------------------------
        self.actionEntropy.setObjectName("actionEntropy")
        self.actionPrivateKey.setObjectName("actionPrivateKey")
        self.actionPublicKey_coordinates.setObjectName("actionPublicKey_coordinates")
        self.actionPublicKey.setObjectName("actionPublicKey")
        self.actionMnemonic.setObjectName("actionMnemonic")

        self.actionNew_random_account.setObjectName("actionNew_random_account")
        self.actionRecover_from_mnemonic.setObjectName("actionRecover_from_mnemonic")
        self.actionRecover_from_entropy.setObjectName("actionRecover_from_entropy")
        self.actionRecover_from_privateKey.setObjectName("actionRecover_from_privateKey")
        # ----------------------------------------------------------------------------------
        self.action_checkTX.setObjectName("action_checkTX")
        self.actionTX_nonce.setObjectName("actionTX_nonce")
        self.actionSimple_history.setObjectName("actionSimple_history")
        self.actionAll_normal.setObjectName("actionAll_normal")
        self.actionAll_internal.setObjectName("actionAll_internal")

        self.actionPublicKey_from_TXHash.setObjectName("actionPublicKey_from_TXHash")
        self.actionTransactionMessage.setObjectName('actionTransactionMessage')
        # ----------------------------------------------------------------------------------
        self.menubar_file.setObjectName("menubar_file")
        self.menubar_file.setGeometry(QRect(0, 0, 800, 25))
        # ----------------------------------------------------------------------------------
        # wallet menu
        self.menubar_file.addAction(self.menu_Wallet.menuAction())
        self.menu_Wallet.setObjectName("menu_Wallet")
        self.menu_Wallet.setTitle("&Wallet")

        #  wallet menu -> account menu
        self.menu_Wallet.addAction(self.menuNew_account.menuAction())
        self.menuNew_account.setObjectName("menuNew_account")
        self.menuNew_account.setTitle("New account")
        self.menuNew_account.addAction(self.actionNew_random_account)
        self.actionNew_random_account.setText("New random account")
        self.menuNew_account.addAction(self.actionRecover_from_mnemonic)
        self.actionRecover_from_mnemonic.setText("Recover from mnemonic")
        self.menuNew_account.addAction(self.actionRecover_from_entropy)
        self.actionRecover_from_entropy.setText("Recover from entropy")
        self.menuNew_account.addAction(self.actionRecover_from_privateKey)
        self.actionRecover_from_privateKey.setText("Recover from privateKey")

        #  wallet menu -> Secrets menu
        self.menu_Wallet.addAction(self.menuSecrets.menuAction())
        self.menuSecrets.setObjectName("menuSecrets")
        self.menuSecrets.setTitle("Secrets")
        self.menuSecrets.addSeparator()
        self.menuSecrets.addAction(self.actionEntropy)
        self.actionEntropy.setText("Entropy")
        self.menuSecrets.addAction(self.actionPrivateKey)
        self.actionPrivateKey.setText("PrivateKey")
        self.menuSecrets.addAction(self.actionPublicKey_coordinates)
        self.actionPublicKey_coordinates.setText("PublicKey coordinates")
        self.menuSecrets.addAction(self.actionPublicKey)
        self.actionPublicKey.setText('PublicKey')
        self.menuSecrets.addAction(self.actionMnemonic)
        self.actionMnemonic.setText("Mnemonic")
        # ----------------------------------------------------------------------------------
        # Network menu
        self.menubar_file.addAction(self.menuNetwork.menuAction())
        self.menuNetwork.setObjectName("menuNetwork")
        self.menuNetwork.setTitle("&Network")

        # Network menu -> Transactions menu
        self.menuNetwork.addAction(self.menuTransactions.menuAction())
        self.menuTransactions.setObjectName("menuTransactions")
        self.menuTransactions.setTitle("Transactions")
        self.menuTransactions.addAction(self.action_checkTX)
        self.action_checkTX.setText("Check transaction")
        self.menuTransactions.addAction(self.actionTX_nonce)
        self.actionTX_nonce.setText("Transaction nounce")
        self.menuTransactions.addAction(self.actionSimple_history)
        self.actionSimple_history.setText("Simple history(need APIkey)")
        self.menuTransactions.addAction(self.actionAll_normal)
        self.actionAll_normal.setText("All normal TXS (need APIkey)")
        self.menuTransactions.addAction(self.actionAll_internal)
        self.actionAll_internal.setText("All internal TXS (need APIkey)")

        # Network menu -> Tools menu
        self.menuNetwork.addAction(self.menuTools.menuAction())
        self.menuTools.setObjectName("menuTools")
        self.menuTools.setTitle("Tools")
        self.menuTools.addAction(self.actionPublicKey_from_TXHash)
        self.actionPublicKey_from_TXHash.setText("PublicKey from TXHash")
        self.menuTools.addAction(self.actionTransactionMessage)
        self.actionTransactionMessage.setText('Show transaction message')
        # ----------------------------------------------------------------------------------
        # row 1
        self.label_node_provider.setObjectName("label_node_provider")
        self.label_node_provider.setText("Node provider:")
        self.lineEdit_node_provider.setText("https://nodes.mewapi.io/rpc/eth")
        self.lineEdit_node_provider.setObjectName("lineEdit_node_provider")
        self.pushButton_node_provider.setObjectName("pushButton_node_provider")
        self.pushButton_node_provider.setText("Providers")

        # row 2
        self.label_accountName.setObjectName("label_accountName")
        self.label_accountName.setText("Account name:")
        self.lineEdit_accountName.setObjectName("lineEdit_accountName")
        self.pushButton_accountName.setObjectName("pushButton_accountName")
        self.pushButton_accountName.setText("Edit")

        # row 3
        self.label_activeAddress.setObjectName("label_activeAddress")
        self.label_activeAddress.setText("Active address:")
        self.comboBox_activeAddress_val.setObjectName(u"comboBox_activeAddress_val")
        self.pushButton_copy_address.setObjectName("pushButton_copy_address")
        self.pushButton_copy_address.setText("Copy address")

        # row 4
        self.label_amount.setObjectName("label_amount")
        self.label_amount.setText("Amount:")
        self.label_amount_val.setObjectName("label_amount_val")
        self.label_amount_val.setText("0")
        self.pushButton_ETH.setObjectName("pushButton_ETH")
        self.pushButton_ETH.setText("etherescan.io")

        # row 5
        self.label_send.setObjectName("label_send")
        self.label_send.setText("Send ETH to:")
        self.lineEdit_send.setObjectName("lineEdit_send")

        # row 6
        self.label_sendValue.setObjectName("label_sendValue")
        self.label_sendValue.setText("Value to send:")
        self.lineEdit_sendValue.setObjectName("lineEdit_sendValue")
        self.pushButton_send.setObjectName("pushButton_send")
        self.pushButton_send.setText("Send TX")
        self.label_message.setObjectName("label_message")
        self.label_message.setText("Message:")
        self.LineEdit_message.setObjectName("LineEdit_message")

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
        # self.line_vertical.setFrameShape(QFrame.VLine)
        # self.line_vertical.setFrameShadow(QFrame.Sunken)
        # ----------------------------------------------------------------------------------
        self.setStatusBar(self.statusbar)
        self.statusbar.setObjectName(u"statusbar")
        # ----------------------------------------------------------------------------------
        # row 1
        self.gridlayout.addWidget(self.label_node_provider, 1, 0, 1, 1)
        self.gridlayout.addWidget(self.lineEdit_node_provider, 1, 1, 1, 3)
        self.gridlayout.addWidget(self.pushButton_node_provider, 1, 4, 1, 1)
        self.gridlayout.addWidget(self.line_vertical, 1, 5, 7, 1)
        self.gridlayout.addWidget(self.label_customizationArea, 1, 6, 1, 1)

        # row 2
        self.gridlayout.addWidget(self.label_accountName, 2, 0, 1, 1)
        self.gridlayout.addWidget(self.lineEdit_accountName, 2, 1, 1, 3)
        self.gridlayout.addWidget(self.pushButton_accountName, 2, 4, 1, 1)
        # col 5 empty
        self.gridlayout.addWidget(self.radioButton_mainNet, 2, 6, 1, 1)

        # row 3
        self.gridlayout.addWidget(self.label_activeAddress, 3, 0, 1, 1)
        self.gridlayout.addWidget(self.comboBox_activeAddress_val, 3, 1, 1, 3)
        self.gridlayout.addWidget(self.pushButton_copy_address, 3, 4, 1, 1)
        # col 5 empty
        self.gridlayout.addWidget(self.radioButton_testNet, 3, 6, 1, 1)

        # row 4
        self.gridlayout.addWidget(self.label_amount, 4, 0, 1, 1)
        self.gridlayout.addWidget(self.label_amount_val, 4, 1, 1, 3)
        self.gridlayout.addWidget(self.pushButton_ETH, 4, 4, 1, 1)
        # col 5 empty
        # col 6 empty

        # row 5
        self.gridlayout.addWidget(self.label_send, 5, 0, 1, 1)
        self.gridlayout.addWidget(self.lineEdit_send, 5, 1, 1, 3)
        # col 3 empty
        # col 4 empty
        # col 5 empty
        # col 6 empty

        # row 6
        self.gridlayout.addWidget(self.label_sendValue, 6, 0, 1, 1)
        self.gridlayout.addWidget(self.lineEdit_sendValue, 6, 1, 1, 1)
        self.gridlayout.addWidget(self.label_message, 6, 2, 1, 1)
        self.gridlayout.addWidget(self.LineEdit_message, 6, 3, 1, 1)
        self.gridlayout.addWidget(self.pushButton_send, 6, 4, 1, 1)
        # col 5 empty
        # col 6 empty

        # row 7
        self.gridlayout.addWidget(self.textEdit_main, 7, 0, 1, 7)

        # self.gridlayout.setRowMinimumHeight(1, 100)
        # self.gridlayout.setRowMinimumHeight(1, 27)
        # self.gridlayout.setRowMinimumHeight(2, 27)
        # self.gridlayout.setRowMinimumHeight(3, 27)
        # self.gridlayout.setRowMinimumHeight(4, 27)
        # self.gridlayout.setRowMinimumHeight(5, 27)
        # self.gridlayout.setRowMinimumHeight(6, 700)
        height = 27
        self.label_node_provider.setMinimumHeight(height)
        self.lineEdit_node_provider.setMinimumHeight(height)
        self.pushButton_node_provider.setMinimumHeight(height)

        self.label_accountName.setMinimumHeight(height)
        self.lineEdit_accountName.setMinimumHeight(height)
        self.pushButton_accountName.setMinimumHeight(height)

        self.label_activeAddress.setMinimumHeight(height)
        self.comboBox_activeAddress_val.setMinimumHeight(height)
        self.pushButton_copy_address.setMinimumHeight(height)

        self.label_amount.setMinimumHeight(height)
        self.label_amount_val.setMinimumHeight(height)
        self.pushButton_ETH.setMinimumHeight(height)

        self.label_send.setMinimumHeight(height)
        self.lineEdit_send.setMinimumHeight(height)

        self.label_sendValue.setMinimumHeight(height)
        self.lineEdit_sendValue.setMinimumHeight(height)
        self.label_message.setMinimumHeight(height)
        self.LineEdit_message.setMinimumHeight(height)
        self.pushButton_send.setMinimumHeight(height)

        # self.textEdit_main.setMinimumHeight(400)
        # self.textEdit_main.resize(780, 400)

        self.setStyleSheet("background-color: rgb(30, 40, 50);")
        self.textEdit_main.setStyleSheet("background-color: black; color: cyan")

        self.comboBox_activeAddress_val.clear()

        self.lineEdit_node_provider.setText('https://rpc.sepolia.org')
        self.lineEdit_node_provider.setStyleSheet('background-color: white; color: black;')

        self.radioButton_mainNet.setChecked(False)
        self.radioButton_testNet.setChecked(True)

        self.lineEdit_accountName.setEnabled(False)
        self.lineEdit_accountName.setStyleSheet("color: yellow; border: none")

        self.pushButton_accountName.setText('Edit')
        self.lineEdit_accountName.setStyleSheet('background-color: rgb(30, 40, 50); color: white; border: none;')

        self.label_amount_val.setText(
            '<span style = "color: red; font-weight: bold;" > 0'
            '</ span> <span style = "color: rgb(140, 170, 250); font-weight: bold;" > ETH </ span>')

        self.radioButton_mainNet.setStyleSheet(f"QRadioButton::indicator:unchecked{{"
                                               f"border: 1px solid red;"
                                               f"}}"
                                               f"QRadioButton::indicator:checked{{"
                                               f"border: 1px solid green;"
                                               f"background-image : url("
                                               f"{system.getIconPath('fill.png')}"
                                               f")}}"
                                               f"QRadioButton::indicator:checked:pressed{{"
                                               f"border: 1px solid white;"
                                               f"}};")

        self.radioButton_testNet.setStyleSheet(f"QRadioButton::indicator:unchecked{{"
                                               f"border: 1px solid red;"
                                               f"}}"
                                               f"QRadioButton::indicator:checked{{"
                                               f"border: 1px solid green;"
                                               f"background-image : url("
                                               f"{system.getIconPath('fill.png')}"
                                               f")}}"
                                               f"QRadioButton::indicator:checked:pressed{{"
                                               f"border: 1px solid white;"
                                               f"}};")

        self.lineEdit_send.setStyleSheet('background-color: rgb(250, 240, 200); color: black')
        self.lineEdit_sendValue.setStyleSheet('background-color: rgb(250, 240, 200); color: black')
        self.LineEdit_message.setStyleSheet('background-color: rgb(250, 240, 200); color: black')

        self.initIcons()
        self.setClickEvents()
        self.setMenuActions()

    def setClickEvents(self):
        self.pushButton_copy_address.clicked.connect(self.copyAddress)
        self.pushButton_ETH.clicked.connect(self.goToEtherscan)
        self.pushButton_node_provider.clicked.connect(self.goToEtherNodes)
        self.pushButton_accountName.clicked.connect(self.editAccountName)
        self.pushButton_send.clicked.connect(self.sendTransaction)
        # Wallets-New wallet---------------------------------------------------------------------------------
        self.actionNew_random_account.triggered.connect(self.createAccountRandom)
        self.actionRecover_from_mnemonic.triggered.connect(self.createAccountFromMnemonic)
        self.actionRecover_from_entropy.triggered.connect(self.createAccountFromEntropy)
        self.actionRecover_from_privateKey.triggered.connect(self.createAccountFromPrivateKey)
        # Wallets-Secrets---------------------------------------------------------------------------------
        self.actionEntropy.triggered.connect(lambda: self.showSecrets(dataTypes.SECRET.ENTROPY))
        self.actionPrivateKey.triggered.connect(lambda: self.showSecrets(dataTypes.SECRET.PRIVATE_KEY))
        self.actionPublicKey_coordinates.triggered.connect(lambda: self.showSecrets(dataTypes.SECRET.PUBLIC_KEY_X))
        self.actionPublicKey.triggered.connect(lambda: self.showSecrets(dataTypes.SECRET.PUBLIC_KEY))
        self.actionMnemonic.triggered.connect(lambda: self.showSecrets(dataTypes.SECRET.MNEMONIC))
        # Network-Transactions---------------------------------------------------------------------------------
        self.action_checkTX.triggered.connect(self.showCustomTransaction)
        self.actionTX_nonce.triggered.connect(self.showNonce)
        self.actionSimple_history.triggered.connect(self.showSimpleHistory)
        self.actionAll_normal.triggered.connect(self.showNormalTransactions)
        self.actionAll_internal.triggered.connect(self.showInternalTransactions)
        # Network-Tools---------------------------------------------------------------------------------
        self.actionPublicKey_from_TXHash.triggered.connect(self.showSenderPublicKey)
        self.actionTransactionMessage.triggered.connect(self.showCustomTransactionMessage)
        # ----------------------------------------------------------------------------------
        self.radioButton_mainNet.toggled.connect(self.changeNetwork)
        self.radioButton_testNet.toggled.connect(self.changeNetwork)
        # ----------------------------------------------------------------------------------
        self.lineEdit_sendValue.textChanged.connect(self.lineEditSendValueChange)
        self.comboBox_activeAddress_val.currentTextChanged.connect(self.comboBoxChange)

    def initIcons(self):
        icon = QIcon()
        size = 20

        icon.addPixmap(QPixmap(system.getIconPath('copy_w.png')))
        self.pushButton_copy_address.setIcon(icon)
        self.pushButton_copy_address.setIconSize(QSize(size, size))

        icon.addPixmap(QPixmap(system.getIconPath('ethereum_c_b.png')))
        self.pushButton_ETH.setIcon(icon)
        self.pushButton_ETH.setIconSize(QSize(size, size))

        icon.addPixmap(QPixmap(system.getIconPath('node64.png')))
        self.pushButton_node_provider.setIcon(icon)
        self.pushButton_node_provider.setIconSize(QSize(size, size))

        icon.addPixmap(QPixmap(system.getIconPath('moneyTransfer48.png')))
        self.pushButton_send.setIcon(icon)
        self.pushButton_send.setIconSize(QSize(size, size))

        icon.addPixmap(QPixmap(system.getIconPath('edit40.png')))
        self.pushButton_accountName.setIcon(icon)
        self.pushButton_node_provider.setIconSize(QSize(size, size))

    def setMenuActions(self):
        self.actionNew_random_account.setShortcut('Ctrl+n')
        self.actionNew_random_account.setStatusTip('create new random account')
        self.actionRecover_from_mnemonic.setShortcut('Ctrl+m')
        self.actionRecover_from_mnemonic.setStatusTip('create new account from mnemonic')
        self.actionRecover_from_entropy.setShortcut('Ctrl+e')
        self.actionRecover_from_entropy.setStatusTip('create new account from entropy')
        self.actionRecover_from_privateKey.setShortcut('Ctrl+p')
        self.actionRecover_from_privateKey.setStatusTip('create new account from privateKey')
        # ----------------------------------------------------------------------------------
        self.actionEntropy.setShortcut('Alt+e')
        self.actionEntropy.setStatusTip('show account entropy')
        self.actionPrivateKey.setShortcut('Alt+v')
        self.actionPrivateKey.setStatusTip('show account privateKey')
        self.actionPublicKey_coordinates.setShortcut('Alt+c')
        self.actionPublicKey_coordinates.setStatusTip('show account publicKey coordinates')
        self.actionPublicKey.setShortcut('Alt+p')
        self.actionPublicKey.setStatusTip('show account publicKey')
        self.actionMnemonic.setShortcut('Alt+m')
        self.actionMnemonic.setStatusTip('show account mnemonic')
        # ----------------------------------------------------------------------------------

    def changeNetwork(self):
        try:
            if self.radioButton_mainNet.isChecked() and not self.radioButton_testNet.isChecked():
                self.lineEdit_node_provider.setText('https://nodes.mewapi.io/rpc/eth')
            elif not self.radioButton_mainNet.isChecked() and self.radioButton_testNet.isChecked():
                self.lineEdit_node_provider.setText('https://rpc.sepolia.org')
            else:
                raise
        except Exception as er:
            gui_errorDialog.Error('changeNetwork', str(er)).exec()

    def comboBoxChange(self):
        try:
            accountName = self.db.readColumnByCondition('NAM', self.comboBox_activeAddress_val.currentText())
            self.lineEdit_accountName.setText(str(accountName[0][0]))
        except Exception as er:
            gui_errorDialog.Error('comboBoxChange', str(er)).exec()

    def editAccountName(self):
        try:
            icon = QIcon()
            if self.pushButton_accountName.text() == 'Edit':
                self.lineEdit_accountName.setEnabled(True)
                self.lineEdit_accountName.setStyleSheet('background-color: rgb(250, 240, 200); color: black')
                self.pushButton_accountName.setText('Save')
                icon.addPixmap(QPixmap(system.getIconPath('save48.png')))
                self.pushButton_accountName.setIcon(icon)
                self.pushButton_node_provider.setIconSize(QSize(16, 16))
            elif self.pushButton_accountName.text() == 'Save':
                self.lineEdit_accountName.setEnabled(False)
                self.lineEdit_accountName.setStyleSheet(
                    'background-color: rgb(30, 40, 50); color: white; border: none;')
                self.pushButton_accountName.setText('Edit')
                icon.addPixmap(QPixmap(system.getIconPath('edit40.png')))
                self.pushButton_accountName.setIcon(icon)
                self.pushButton_node_provider.setIconSize(QSize(16, 16))
                self.db.updateRowValue(columnName='NAM',
                                       newValue=self.lineEdit_accountName.text(),
                                       condition=self.comboBox_activeAddress_val.currentText())
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
                        self.comboBox_activeAddress_val.addItem(acc['address'])
                        self.comboBox_activeAddress_val.setCurrentIndex(self.comboBox_activeAddress_val.count() - 1)
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
                        self.comboBox_activeAddress_val.addItem(acc['address'])
                        self.comboBox_activeAddress_val.setCurrentIndex(self.comboBox_activeAddress_val.count() - 1)
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
                        self.comboBox_activeAddress_val.addItem(acc['address'])
                        self.comboBox_activeAddress_val.setCurrentIndex(self.comboBox_activeAddress_val.count() - 1)
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
                        self.comboBox_activeAddress_val.addItem(acc['address'])
                        self.comboBox_activeAddress_val.setCurrentIndex(self.comboBox_activeAddress_val.count() - 1)
                    else:
                        pass  # Inserting account details to database failed
        except Exception as er:
            gui_errorDialog.Error('createAccountFromMnemonic', str(er)).exec()

    def goToEtherscan(self):
        try:
            active_address = self.comboBox_activeAddress_val.currentText()
            if active_address is None:
                gui_errorDialog.Error('goToEtherscan', 'No address selected').exec()
            else:
                if self.radioButton_mainNet.isChecked() and not self.radioButton_testNet.isChecked():
                    open('https://etherscan.io/address/' + active_address)
                elif not self.radioButton_mainNet.isChecked() and self.radioButton_testNet.isChecked():
                    open('https://sepolia.etherscan.io/address/' + active_address)
                else:
                    gui_errorDialog.Error('goToEtherscan', 'Unknown network').exec()
        except Exception as er:
            gui_errorDialog.Error('goToEtherscan', str(er)).exec()

    def goToEtherNodes(self):
        try:
            if self.radioButton_mainNet.isChecked() and not self.radioButton_testNet.isChecked():
                open('https://ethereumnodes.com/')
            elif not self.radioButton_mainNet.isChecked() and self.radioButton_testNet.isChecked():
                open('https://sepolia.dev/')
            else:
                gui_errorDialog.Error('goToEtherNodes', 'Unknown network').exec()
        except Exception as er:
            gui_errorDialog.Error('goToEtherNodes', str(er)).exec()

    def copyAddress(self):
        try:
            active_address = self.comboBox_activeAddress_val.currentText()
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
                        dataTypes.SECRET.ENTROPY.value, self.comboBox_activeAddress_val.currentText()
                    ) == self.db.readColumnByCondition(dataTypes.SECRET.PRIVATE_KEY.value,
                                                       self.comboBox_activeAddress_val.currentText())):
                qui_showMessage.Ui('Show secrets',
                                   'You have recovered an old account.',
                                   'Entropy is not recoverable from private key').exec()
            elif secretType == dataTypes.SECRET.MNEMONIC and (
                    self.db.readColumnByCondition(
                        dataTypes.SECRET.MNEMONIC.value, self.comboBox_activeAddress_val.currentText()
                    ) == self.db.readColumnByCondition(dataTypes.SECRET.PRIVATE_KEY.value,
                                                       self.comboBox_activeAddress_val.currentText())):
                qui_showMessage.Ui('Show secrets',
                                   'You have recovered an old account.',
                                   'Mnemonic is not recoverable from private key').exec()
            elif secretType == dataTypes.SECRET.PUBLIC_KEY_X or secretType == dataTypes.SECRET.PUBLIC_KEY_Y:
                result_X = self.db.readColumnByCondition(dataTypes.SECRET.PUBLIC_KEY_X.value,
                                                         self.comboBox_activeAddress_val.currentText())
                result_Y = self.db.readColumnByCondition(dataTypes.SECRET.PUBLIC_KEY_Y.value,
                                                         self.comboBox_activeAddress_val.currentText())
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
                                                       self.comboBox_activeAddress_val.currentText())
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
            balance = ethereum.getBalance(self.comboBox_activeAddress_val.currentText(),
                                          self.lineEdit_node_provider.text())
            if balance < 0:
                pass  # error in getting balance
            else:
                color = 'red'
                if balance > 0:
                    color = 'green'
                self.label_amount_val.setText(
                    '<span style = "color: ' + color + '; font-weight: bold;" > ' + str(balance) +
                    '</ span> <span style = "color: rgb(140, 170, 250); font-weight: bold;" > ETH </ span>')
                print('balance = ', balance)
        except Exception as er:
            gui_errorDialog.Error('getBalance', str(er)).exec()

    def sendTransaction(self, isContract: bool = False):
        if not self.LineEdit_message.text() == '' or not self.lineEdit_sendValue.text() == '':
            if self.lineEdit_send.text() == '' and isContract:  # deploy contract
                pass
            elif self.lineEdit_send.text() == '' and not isContract:  # send transaction need address
                qui_showMessage.Ui('sendTransaction', "Enter the recipient\'s address").exec()
                return {}
            else:
                if self.LineEdit_message.text() == '':  # it is normal transaction
                    if self.lineEdit_sendValue.text() == '':
                        qui_showMessage.Ui('sendTransaction', "Enter value to send").exec()
                        return {}
                    else:
                        self.sentETH()
                elif not self.LineEdit_message.text() == '':  # it is message transaction
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
            transactions = self.transactionElements(data=self.LineEdit_message.text().encode("utf-8").hex())
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
                    'sender': self.comboBox_activeAddress_val.currentText(),
                    'receiver': self.lineEdit_send.text(),
                    'vale': val,
                    'provider': self.lineEdit_node_provider.text(),
                    'chainId': chainId,
                    'data': data
                }
            else:
                pass  # network selection error
        except Exception as er:
            gui_errorDialog.Error('transactionElements', str(er)).exec()

    def showTransaction(self, txHash):
        try:
            tx = ethereum.getTransaction(txHash, self.lineEdit_node_provider.text())
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
            tx = ethereum.getTransaction(txHash, self.lineEdit_node_provider.text())
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
            nonce = ethereum.getAccountNonce(self.comboBox_activeAddress_val.currentText(),
                                             self.lineEdit_node_provider.text())
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

            txHistory = ethereum.getNormalHistory(self.comboBox_activeAddress_val.currentText(),
                                                  self.lineEdit_node_provider.text(), APIkey, mainNet)
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
            txHistory = ethereum.getInternalHistory(self.comboBox_activeAddress_val.currentText(),
                                                    self.lineEdit_node_provider.text(), APIkey, mainNet)
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

                if len(txHistoryNormal) > 0 or len(txHistoryInternal) > 0: #  there is something for show
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
                result = ethereum.getPublicKeyFromTransaction(TxHash, self.lineEdit_node_provider.text())
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
