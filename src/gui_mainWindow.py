from webbrowser import open
from pyperclip import copy
from PyQt6.QtWidgets import QFrame
from json import loads
from PyQt6 import QtWidgets, uic
from PyQt6.QtCore import QSize, QRect
from PyQt6.QtGui import QIcon, QPixmap, QAction, QTextCursor
from src import (database, types, gui_errorDialog, qui_getUserChoice, qui_getUserInput, qui_showMessage, ethereum,
                 account)


class Ui(QtWidgets.QMainWindow):
    def __init__(self, dbName):
        super().__init__()
        uic.loadUi('resources/UI/MainWindow.ui', self)

        self.gridlayout = self.findChild(QtWidgets.QGridLayout, 'gridlayout')
        self.line_vertical = self.findChild(QFrame, 'gridlayout')
        # ----------------------------------------------------------------------------------
        self.actionEntropy = self.findChild(QAction, 'actionEntropy')
        self.actionPrivateKey = self.findChild(QAction, 'actionPrivateKey')
        self.actionPublicKey_coordinates = self.findChild(QAction, 'actionPublicKey_coordinates')
        self.actionPublicKey = self.findChild(QAction, 'actionPublicKey')
        self.actionMnemonic = self.findChild(QAction, 'actionMnemonic')

        self.actionNew_random_account = self.findChild(QAction, 'actionNew_random_account')
        self.actionRecover_from_mnemonic = self.findChild(QAction, 'actionRecover_from_mnemonic')
        self.actionRecover_from_entropy = self.findChild(QAction, 'actionRecover_from_entropy')
        self.actionRecover_from_privateKey = self.findChild(QAction, 'actionRecover_from_privateKey')

        self.action_checkTX = self.findChild(QAction, 'action_checkTX')
        self.actionTX_nonce = self.findChild(QAction, 'actionTX_nonce')
        self.actionSimple_history = self.findChild(QAction, 'actionSimple_history')
        self.actionAll_normal = self.findChild(QAction, 'actionAll_normal')
        self.actionAll_internal = self.findChild(QAction, 'actionAll_internal')

        self.actionPublicKey_from_TXHash = self.findChild(QAction, 'actionPublicKey_from_TXHash')
        # ----------------------------------------------------------------------------------
        self.label_customizationArea = self.findChild(QtWidgets.QLabel, 'label_customizationArea')
        self.radioButton_mainNet = self.findChild(QtWidgets.QRadioButton, 'radioButton_mainNet')
        self.radioButton_testNet = self.findChild(QtWidgets.QRadioButton, 'radioButton_testNet')
        # ----------------------------------------------------------------------------------
        self.label_node_provider = self.findChild(QtWidgets.QLabel, 'label_node_provider')
        self.lineEdit_node_provider = self.findChild(QtWidgets.QLineEdit, 'lineEdit_node_provider')
        self.pushButton_node_provider = self.findChild(QtWidgets.QPushButton, 'pushButton_node_provider')

        self.label_accountName = self.findChild(QtWidgets.QLabel, 'label_accountName')
        self.lineEdit_accountName = self.findChild(QtWidgets.QLineEdit, 'lineEdit_accountName')
        self.pushButton_accountName = self.findChild(QtWidgets.QPushButton, 'pushButton_accountName')

        self.label_activeAddress = self.findChild(QtWidgets.QLabel, 'label_activeAddress')
        self.comboBox_activeAddress_val = self.findChild(QtWidgets.QComboBox, 'comboBox_activeAddress_val')
        self.pushButton_copy_address = self.findChild(QtWidgets.QPushButton, 'pushButton_copy_address')

        self.label_amount = self.findChild(QtWidgets.QLabel, 'label_amount')
        self.label_amount_val = self.findChild(QtWidgets.QLabel, 'label_amount_val')
        self.pushButton_ETH = self.findChild(QtWidgets.QPushButton, 'pushButton_ETH')

        self.label_send = self.findChild(QtWidgets.QLabel, 'label_send')
        self.lineEdit_send = self.findChild(QtWidgets.QLineEdit, 'lineEdit_send')

        self.label_value = self.findChild(QtWidgets.QLabel, 'label_value')
        self.lineEdit_sendValue = self.findChild(QtWidgets.QLineEdit, 'lineEdit_sendValue')
        self.label_estimated = self.findChild(QtWidgets.QLabel, 'label_estimated')
        self.label_gasEstimated_val = self.findChild(QtWidgets.QLabel, 'label_gasEstimated_val')
        self.pushButton_send = self.findChild(QtWidgets.QPushButton, 'pushButton_send')
        # ----------------------------------------------------------------------------------
        self.textEdit_main = self.findChild(QtWidgets.QTextEdit, 'textEdit_main')

        self.db = database.Sqlite(dbName)
        self.initUI()

    def initUI(self):
        self.resize(800, 600)
        self.gridlayout.setGeometry(QRect(10, 10, 780, 580))
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

        self.label_value.setMinimumHeight(height)
        self.lineEdit_sendValue.setMinimumHeight(height)
        self.label_estimated.setMinimumHeight(height)
        self.label_gasEstimated_val.setMinimumHeight(height)
        self.pushButton_send.setMinimumHeight(height)

        # self.textEdit_main.setMinimumHeight(400)
        # self.textEdit_main.resize(780, 400)

        self.setStyleSheet("background-color: rgb(30, 40, 50);")
        self.textEdit_main.setStyleSheet("background-color: black; color: cyan")

        self.comboBox_activeAddress_val.clear()

        self.lineEdit_node_provider.setText('https://nodes.mewapi.io/rpc/eth')
        self.lineEdit_node_provider.setStyleSheet('background-color: white; color: black;')

        self.radioButton_mainNet.setChecked(True)

        self.radioButton_testNet.setChecked(False)

        self.lineEdit_accountName.setEnabled(False)
        self.lineEdit_accountName.setStyleSheet("color: yellow; border: none")

        self.pushButton_accountName.setText('Edit')
        self.lineEdit_accountName.setStyleSheet('background-color: rgb(30, 40, 50); color: white; border: none;')

        self.label_amount_val.setText(
            '<span style = "color: red; font-weight: bold;" > 0'
            '</ span> <span style = "color: rgb(140, 170, 250); font-weight: bold;" > ETH </ span>')

        self.radioButton_mainNet.setStyleSheet("QRadioButton::indicator:unchecked{"
                                               "border: 1px solid red;"
                                               "}"
                                               "QRadioButton::indicator:checked{"
                                               "border: 1px solid green;"
                                               "background-image : url(resources/UI/icons/fill.png)"
                                               "}"
                                               "QRadioButton::indicator:checked:pressed{"
                                               "border: 1px solid white;"
                                               "};")

        self.radioButton_testNet.setStyleSheet("QRadioButton::indicator:unchecked{"
                                               "border: 1px solid red;"
                                               "}"
                                               "QRadioButton::indicator:checked{"
                                               "border: 1px solid green;"
                                               "background-image : url(resources/UI/icons/fill.png)"
                                               "}"
                                               "QRadioButton::indicator:checked:pressed{"
                                               "border: 1px solid white;"
                                               "};")

        self.lineEdit_send.setStyleSheet('background-color: rgb(250, 240, 200); color: black')
        self.lineEdit_sendValue.setStyleSheet('background-color: rgb(250, 240, 200); color: black')

        self.initIcons()
        self.setClickEvents()
        self.setMenuActions()

    def setClickEvents(self):
        self.pushButton_copy_address.clicked.connect(self.copyAddress)
        self.pushButton_ETH.clicked.connect(self.goToEtherscan)
        self.pushButton_node_provider.clicked.connect(self.goToEtherNodes)
        self.pushButton_accountName.clicked.connect(self.editAccountName)
        self.pushButton_send.clicked.connect(self.sentETH)
        # Wallets-New wallet---------------------------------------------------------------------------------
        self.actionNew_random_account.triggered.connect(self.createAccountRandom)
        self.actionRecover_from_mnemonic.triggered.connect(self.createAccountFromMnemonic)
        self.actionRecover_from_entropy.triggered.connect(self.createAccountFromEntropy)
        self.actionRecover_from_privateKey.triggered.connect(self.createAccountFromPrivateKey)
        # Wallets-Secrets---------------------------------------------------------------------------------
        self.actionEntropy.triggered.connect(lambda: self.showSecrets(types.SECRET.ENTROPY))
        self.actionPrivateKey.triggered.connect(lambda: self.showSecrets(types.SECRET.PRIVATE_KEY))
        self.actionPublicKey_coordinates.triggered.connect(lambda: self.showSecrets(types.SECRET.PUBLIC_KEY_X))
        self.actionPublicKey.triggered.connect(lambda: self.showSecrets(types.SECRET.PUBLIC_KEY))
        self.actionMnemonic.triggered.connect(lambda: self.showSecrets(types.SECRET.MNEMONIC))
        # Network-Transactions---------------------------------------------------------------------------------
        self.action_checkTX.triggered.connect(self.showCustomTransaction)
        self.actionTX_nonce.triggered.connect(self.showNonce)
        self.actionSimple_history.triggered.connect(self.showSimpleHistory)
        self.actionAll_normal.triggered.connect(self.showNormalTransactions)
        self.actionAll_internal.triggered.connect(self.showInternalTransactions)
        # Network-Tools---------------------------------------------------------------------------------
        self.actionPublicKey_from_TXHash.triggered.connect(self.showSenderPublicKey)
        # ----------------------------------------------------------------------------------
        self.radioButton_mainNet.toggled.connect(self.changeNetwork)
        self.radioButton_testNet.toggled.connect(self.changeNetwork)
        # ----------------------------------------------------------------------------------
        self.lineEdit_sendValue.textChanged.connect(self.lineEditSendValueChange)
        self.comboBox_activeAddress_val.currentTextChanged.connect(self.comboBoxChange)

    def initIcons(self):
        icon = QIcon()
        size = 20

        icon.addPixmap(QPixmap('resources/UI/icons/copy_w.png'))
        self.pushButton_copy_address.setIcon(icon)
        self.pushButton_copy_address.setIconSize(QSize(size, size))

        icon.addPixmap(QPixmap('resources/UI/icons/ethereum_c_b.png'))
        self.pushButton_ETH.setIcon(icon)
        self.pushButton_ETH.setIconSize(QSize(size, size))

        icon.addPixmap(QPixmap('resources/UI/icons/node64.png'))
        self.pushButton_node_provider.setIcon(icon)
        self.pushButton_node_provider.setIconSize(QSize(size, size))

        icon.addPixmap(QPixmap('resources/UI/icons/moneyTransfer48.png'))
        self.pushButton_send.setIcon(icon)
        self.pushButton_send.setIconSize(QSize(size, size))

        icon.addPixmap(QPixmap('resources/UI/icons/edit40.png'))
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
                icon.addPixmap(QPixmap('resources/UI/icons/save48.png'))
                self.pushButton_accountName.setIcon(icon)
                self.pushButton_node_provider.setIconSize(QSize(16, 16))
            elif self.pushButton_accountName.text() == 'Save':
                self.lineEdit_accountName.setEnabled(False)
                self.lineEdit_accountName.setStyleSheet(
                    'background-color: rgb(30, 40, 50); color: white; border: none;')
                self.pushButton_accountName.setText('Edit')
                icon.addPixmap(QPixmap('resources/UI/icons/edit40.png'))
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

    def showSecrets(self, secretType: types.SECRET):
        try:
            self.textEdit_main.clear()
            if secretType == types.SECRET.ENTROPY and (
                    self.db.readColumnByCondition(
                        types.SECRET.ENTROPY.value, self.comboBox_activeAddress_val.currentText()
                    ) == self.db.readColumnByCondition(types.SECRET.PRIVATE_KEY.value,
                                                       self.comboBox_activeAddress_val.currentText())):
                qui_showMessage.Ui('Show secrets',
                                   'You have recovered an old account.',
                                   'Entropy is not recoverable from private key').exec()
            elif secretType == types.SECRET.MNEMONIC and (
                    self.db.readColumnByCondition(
                        types.SECRET.MNEMONIC.value, self.comboBox_activeAddress_val.currentText()
                    ) == self.db.readColumnByCondition(types.SECRET.PRIVATE_KEY.value,
                                                       self.comboBox_activeAddress_val.currentText())):
                qui_showMessage.Ui('Show secrets',
                                   'You have recovered an old account.',
                                   'Mnemonic is not recoverable from private key').exec()
            elif secretType == types.SECRET.PUBLIC_KEY_X or secretType == types.SECRET.PUBLIC_KEY_Y:
                result_X = self.db.readColumnByCondition(types.SECRET.PUBLIC_KEY_X.value,
                                                         self.comboBox_activeAddress_val.currentText())
                result_Y = self.db.readColumnByCondition(types.SECRET.PUBLIC_KEY_Y.value,
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
                    if secretType == types.SECRET.MNEMONIC or secretType == types.SECRET.ENTROPY:
                        self.textEdit_main.append(f'{secretType.name} + Passphrase = your account\n\n'
                                                  f'{secretType.name} without Passphrase = unknown account\n'
                                                  f'(If no passphrase set = your account)')
                    elif secretType == types.SECRET.PRIVATE_KEY:
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
                    transactionHash = ethereum.sendTransaction(privateKey=(self.db.readColumnByCondition(
                        types.SECRET.PRIVATE_KEY.value, transactions['sender']))[0][0], txElements=transactions)
                    if transactionHash == '':
                        pass  # Transaction failed
                    else:
                        qui_showMessage.Ui('Your job is done',
                                           'Transaction succeed:',
                                           f'Hash: {transactionHash}').exec()
                        self.showTransaction(transactionHash)
        except Exception as er:
            gui_errorDialog.Error('sentETH', str(er)).exec()

    def transactionElements(self):
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
                    qui_showMessage.Ui('transaction elements', 'Enter amount!').exec()
                    return {}
                else:
                    return {
                        'sender': self.comboBox_activeAddress_val.currentText(),
                        'receiver': self.lineEdit_send.text(),
                        'vale': float(self.lineEdit_sendValue.text()),
                        'provider': self.lineEdit_node_provider.text(),
                        'chainId': chainId
                    }
            else:
                pass  # select network error
        except Exception as er:
            gui_errorDialog.Error('transactionElements', str(er)).exec()

    def showTransaction(self, txHash):
        try:
            tx = ethereum.getTransaction(txHash, self.lineEdit_node_provider.text())
            if tx == '':
                pass  # error getting transaction
            else:
                self.textEdit_main.clear()
                print(tx)
                print(type(tx))
                tx = loads(tx)  # convert to json
                print(type(tx))
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
