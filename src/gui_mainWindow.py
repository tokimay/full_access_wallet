import webbrowser
import pyperclip
import web3

import src.account as account
from src import database, types, gui_errorDialog, qui_getUserChoice, qui_getUserInput, qui_showMessage
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
        self.radioButton_mainNet = self.findChild(QtWidgets.QRadioButton, 'radioButton_mainNet')
        self.radioButton_testNet = self.findChild(QtWidgets.QRadioButton, 'radioButton_testNet')
        self.label_accountName = self.findChild(QtWidgets.QLabel, 'label_accountName')
        self.lineEdit_accountName = self.findChild(QtWidgets.QLineEdit, 'lineEdit_accountName')
        self.pushButton_accountName = self.findChild(QtWidgets.QPushButton, 'pushButton_accountName')

        self.actionEntropy = self.findChild(QAction, 'actionEntropy')
        self.actionPrivateKey = self.findChild(QAction, 'actionPrivateKey')
        self.actionPublicKey_coordinates = self.findChild(QAction, 'actionPublicKey_coordinates')
        self.actionPublicKey = self.findChild(QAction, 'actionPublicKey')
        self.actionMnemonic = self.findChild(QAction, 'actionMnemonic')

        self.actionNew_random_account = self.findChild(QAction, 'actionNew_random_account')
        self.actionRecover_from_mnemonic = self.findChild(QAction, 'actionRecover_from_mnemonic')
        self.actionRecover_from_entropy = self.findChild(QAction, 'actionRecover_from_entropy')
        self.actionRecover_from_privateKey = self.findChild(QAction, 'actionRecover_from_privateKey')

        self.db = database.Sqlite(dbName)
        self.initUI()

    def initUI(self):
        # self.setStyleSheet("QMainWindow {background-color: gray;}")
        self.setStyleSheet("background-color: rgb(30, 40, 50);")
        self.textEdit_main.setStyleSheet("background-color: black; color: cyan")

        self.comboBox_activeAddress_val.clear()
        self.comboBox_activeAddress_val.currentTextChanged.connect(self.comboBoxChange)

        self.lineEdit_node_provider.setText('https://nodes.mewapi.io/rpc/eth')
        self.lineEdit_node_provider.setStyleSheet('background-color: white; color: black;')

        self.radioButton_mainNet.setChecked(True)

        self.radioButton_testNet.setChecked(False)

        self.lineEdit_accountName.setEnabled(False)
        self.lineEdit_accountName.setStyleSheet("color: yellow; border: none")

        self.pushButton_accountName.setText('Edit')

        self.label_amount_val.setText(
            '<span style = "color: red"; font-weight: bold"; > 0 </ span>'
            '<span style = "color: rgb(140, 170, 250); font-weight: bold;" > ETH </ span>')

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
        self.initIcons()
        self.setClickEvents()
        self.setMenuActions()

    def setClickEvents(self):
        self.pushButton_copy_address.clicked.connect(self.copyAddress)
        self.pushButton_ETH.clicked.connect(self.goToEtherscan)
        self.pushButton_node_provider.clicked.connect(self.goToEtherNodes)
        self.pushButton_accountName.clicked.connect(self.editAccountName)
        # ----------------------------------------------------------------------------------
        self.actionNew_random_account.triggered.connect(self.createAccountRandom)
        self.actionRecover_from_mnemonic.triggered.connect(self.createAccountFromMnemonic)
        self.actionRecover_from_entropy.triggered.connect(self.createAccountFromEntropy)
        self.actionRecover_from_privateKey.triggered.connect(self.createAccountFromPrivateKey)
        # ----------------------------------------------------------------------------------
        self.actionEntropy.triggered.connect(lambda: self.showSecrets(types.SECRET.ENTROPY))
        self.actionPrivateKey.triggered.connect(lambda: self.showSecrets(types.SECRET.PRIVATE_KEY))
        self.actionPublicKey_coordinates.triggered.connect(lambda: self.showSecrets(types.SECRET.PUBLIC_KEY_X))
        self.actionPublicKey.triggered.connect(lambda: self.showSecrets(types.SECRET.PUBLIC_KEY))
        self.actionMnemonic.triggered.connect(lambda: self.showSecrets(types.SECRET.MNEMONIC))
        # ----------------------------------------------------------------------------------
        self.radioButton_mainNet.toggled.connect(self.changeNetwork)
        self.radioButton_testNet.toggled.connect(self.changeNetwork)

    def initIcons(self):
        icon = QIcon()

        icon.addPixmap(QPixmap('resources/UI/icons/copy_w.png'))
        self.pushButton_copy_address.setIcon(icon)
        self.pushButton_copy_address.setIconSize(QSize(16, 16))

        icon.addPixmap(QPixmap('resources/UI/icons/ethereum_c_b.png'))
        self.pushButton_ETH.setIcon(icon)
        self.pushButton_ETH.setIconSize(QSize(16, 16))

        icon.addPixmap(QPixmap('resources/UI/icons/ethereum_node_clr.png'))
        self.pushButton_node_provider.setIcon(icon)
        self.pushButton_node_provider.setIconSize(QSize(16, 16))

        icon.addPixmap(QPixmap('resources/UI/icons/edit40.png'))
        self.pushButton_accountName.setIcon(icon)
        self.pushButton_node_provider.setIconSize(QSize(16, 16))

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
            gui_errorDialog.Error(str(er)).exec()

    def comboBoxChange(self):
        try:
            accountName = self.db.readColumnByCondition('NAM', self.comboBox_activeAddress_val.currentText())
            self.lineEdit_accountName.setText(str(accountName[0][0]))
        except Exception as er:
            gui_errorDialog.Error(str(er)).exec()

    def editAccountName(self):
        try:
            icon = QIcon()
            if self.pushButton_accountName.text() == 'Edit':
                self.lineEdit_accountName.setEnabled(True)
                self.pushButton_accountName.setText('Save')
                icon.addPixmap(QPixmap('resources/UI/icons/save48.png'))
                self.pushButton_accountName.setIcon(icon)
                self.pushButton_node_provider.setIconSize(QSize(16, 16))
            elif self.pushButton_accountName.text() == 'Save':
                self.lineEdit_accountName.setEnabled(False)
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
            gui_errorDialog.Error(str(er)).exec()

    def createAccountRandom(self):
        userAnswer = True
        if self.db.isAccountExist():
            createAccount_window = qui_getUserChoice.Ui('Create new account',
                                                        'Some account(s) already exist',
                                                        'Create new one?')
            createAccount_window.exec()
            userAnswer = createAccount_window.getAnswer()
        if not userAnswer:
            pass  # cancel by user or it is new account
        else:
            acc = account.New.random()  # create new account
            if len(acc) == 0:  # random account creation return by some error
                pass
            elif not isinstance(acc, dict) or len(acc) == 0:
                pass  # Account creation failed
            else:
                if self.db.insertRow(acc):
                    self.comboBox_activeAddress_val.addItem(acc['address'])
                    self.comboBox_activeAddress_val.setCurrentIndex(self.comboBox_activeAddress_val.count() - 1)
                else:
                    gui_errorDialog.Error('Inserting account details to database failed.\n').exec()

    def createAccountFromEntropy(self):
        getEntropy = qui_getUserInput.Ui('Recover account', 'Enter your entropy:')
        getEntropy.exec()
        entropy = getEntropy.getInput()
        if entropy == '':
            (qui_showMessage.Ui('Recover account',
                                'Nothing received',
                                'you can try again from Wallet -> New account -> Recover from entropy')
             .exec())
        else:
            acc = account.New.fromEntropy(entropy)
            if not isinstance(acc, dict) or len(acc) == 0:
                pass  # Account creation failed
            else:
                if self.db.insertRow(acc):
                    self.comboBox_activeAddress_val.addItem(acc['address'])
                    self.comboBox_activeAddress_val.setCurrentIndex(self.comboBox_activeAddress_val.count() - 1)
                else:
                    gui_errorDialog.Error('Inserting account details to database failed.\n').exec()

    def createAccountFromPrivateKey(self):
        getPrivateKey = qui_getUserInput.Ui('Recover account', 'Enter your private key:')
        getPrivateKey.exec()
        privateKey = getPrivateKey.getInput()
        if privateKey == '':
            (qui_showMessage.Ui('Recover account',
                                'Nothing received',
                                'you can try again from Wallet -> New account -> Recover from private key')
             .exec())
        else:
            acc = account.New.fromPrivateKey(privateKey)
            if not isinstance(acc, dict) or len(acc) == 0:
                pass  # Account creation failed
            else:
                if self.db.insertRow(acc):
                    self.comboBox_activeAddress_val.addItem(acc['address'])
                    self.comboBox_activeAddress_val.setCurrentIndex(self.comboBox_activeAddress_val.count() - 1)
                else:
                    gui_errorDialog.Error('Inserting account details to database failed.\n').exec()

    def createAccountFromMnemonic(self):
        getMnemonic = qui_getUserInput.Ui('Recover account', 'Enter your mnemonic:')
        getMnemonic.exec()
        privateKey = getMnemonic.getInput()
        if privateKey == '':
            (qui_showMessage.Ui('Recover account',
                                'Nothing received',
                                'you can try again from Wallet -> New account -> Recover from mnemonic')
             .exec())
        else:
            acc = account.New.fromMnemonic(privateKey)
            if not isinstance(acc, dict) or len(acc) == 0:
                pass  # Account creation failed
            else:
                if self.db.insertRow(acc):
                    self.comboBox_activeAddress_val.addItem(acc['address'])
                    self.comboBox_activeAddress_val.setCurrentIndex(self.comboBox_activeAddress_val.count() - 1)
                else:
                    gui_errorDialog.Error('Inserting account details to database failed.\n').exec()

    def goToEtherscan(self):
        try:
            active_address = self.comboBox_activeAddress_val.currentText()
            if active_address is None:
                raise
            if self.radioButton_mainNet.isChecked() and not self.radioButton_testNet.isChecked():
                webbrowser.open('https://etherscan.io/address/' + active_address)
            elif not self.radioButton_mainNet.isChecked() and self.radioButton_testNet.isChecked():
                webbrowser.open('https://sepolia.etherscan.io/address/' + active_address)
            else:
                raise
        except Exception as er:
            gui_errorDialog.Error(str(er)).exec()

    def goToEtherNodes(self):
        try:
            if self.radioButton_mainNet.isChecked() and not self.radioButton_testNet.isChecked():
                webbrowser.open('https://ethereumnodes.com/')
            elif not self.radioButton_mainNet.isChecked() and self.radioButton_testNet.isChecked():
                webbrowser.open('https://sepolia.dev/')
            else:
                raise
        except Exception as er:
            gui_errorDialog.Error(str(er)).exec()

    def copyAddress(self):
        try:
            active_address = self.comboBox_activeAddress_val.currentText()
            if active_address is not None:
                pyperclip.copy(active_address)
            # spam = pyperclip.paste()
        except Exception as er:
            gui_errorDialog.Error(str(er)).exec()

    def getBalance(self):
        try:
            w3 = web3.Web3(web3.HTTPProvider(self.lineEdit_node_provider.text()))
            address_cksm = web3.Web3.to_checksum_address(self.comboBox_activeAddress_val.currentText())
            balance = w3.eth.get_balance(address_cksm)
            balance = web3.Web3.from_wei(balance, 'ether')
            if balance > 0:
                color = 'green'
            else:
                color = 'red'
            self.label_amount_val.setText(
                '<span style = "color: ' + color + '; font-weight: bold;" > ' + str(balance) +
                '</ span> <span style = "color: rgb(140, 170, 250); font-weight: bold;" > ETH </ span>')

            print('balance = ', balance)
        except Exception as er:
            gui_errorDialog.Error(str(er)).exec()

    def showSecrets(self, secretType: types.SECRET):
        self.textEdit_main.clear()
        if secretType == types.SECRET.PUBLIC_KEY_X or secretType == types.SECRET.PUBLIC_KEY_Y:
            result_X = (self.db.readColumnByCondition(
                columnName=types.SECRET.PUBLIC_KEY_X.value, condition=self.comboBox_activeAddress_val.currentText()))
            result_Y = (self.db.readColumnByCondition(
                columnName=types.SECRET.PUBLIC_KEY_Y.value, condition=self.comboBox_activeAddress_val.currentText()))
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
                columnName=secretType.value, condition=self.comboBox_activeAddress_val.currentText()))
            if len(result) <= 0:
                gui_errorDialog.Error('Reading database failed').exec()
            else:
                if secretType == types.SECRET.ENTROPY and (
                        self.db.readColumnByCondition(columnName=types.SECRET.ENTROPY.value,
                                                      condition=self.comboBox_activeAddress_val.currentText())
                        ==
                        self.db.readColumnByCondition(columnName=types.SECRET.PRIVATE_KEY.value,
                                                      condition=self.comboBox_activeAddress_val.currentText())
                ):
                    qui_showMessage.Ui('Show secrets',
                                       'You have recovered an old account.',
                                       'Entropy is not recoverable from private key').exec()
                elif secretType == types.SECRET.MNEMONIC and (
                        self.db.readColumnByCondition(columnName=types.SECRET.MNEMONIC.value,
                                                      condition=self.comboBox_activeAddress_val.currentText())
                        ==
                        self.db.readColumnByCondition(columnName=types.SECRET.PRIVATE_KEY.value,
                                                      condition=self.comboBox_activeAddress_val.currentText())
                ):
                    qui_showMessage.Ui('Show secrets',
                                       'You have recovered an old account.',
                                       'Mnemonic is not recoverable from private key').exec()
                elif len(result) == 1:
                    self.textEdit_main.append(f'Your account {secretType.name} keep it safe:\n')
                    self.textEdit_main.append(f'{result[0][0]}\n')
                    if secretType == types.SECRET.MNEMONIC or secretType == types.SECRET.ENTROPY:
                        self.textEdit_main.append(f'{secretType.name} + Passphrase = your account\n\n'
                                                  f'{secretType.name} without Passphrase = unknown account')
                    elif secretType == types.SECRET.PRIVATE_KEY:
                        self.textEdit_main.append(f'{secretType.name} = your account')

                else:
                    for res in result:
                        self.textEdit_main.append(f'{res[0]}\n')
                    if secretType == types.SECRET.MNEMONIC or secretType == types.SECRET.ENTROPY:
                        self.textEdit_main.append(f'{secretType.name} + Passphrase = your account\n\n'
                                                  f'{secretType.name} without Passphrase = unknown account')
                    elif secretType == types.SECRET.PRIVATE_KEY:
                        self.textEdit_main.append(f'{secretType.name} = your account')