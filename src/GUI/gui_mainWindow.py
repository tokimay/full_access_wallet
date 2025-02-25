
# This file is part of https://github.com/tokimay/full_access_wallet
# Copyright (C) 2016 https://github.com/tokimay
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
# This software is licensed under GPLv3. If you use or modify this project,
# you must include a reference to the original repository: https://github.com/tokimay/full_access_wallet

from decimal import Decimal
from sys import exit
from pyperclip import copy
from PyQt6.QtWidgets import QFrame, QTabWidget, QMainWindow, QWidget
from json import loads, dump, dumps
from PyQt6.QtCore import QSize, QUrl
from PyQt6.QtGui import QAction, QTextCursor, QPixmap, QIcon
from pathlib import Path
from tkinter import filedialog, Tk
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWidgets import (QGridLayout, QLabel, QPushButton, QComboBox, QLineEdit,
                             QRadioButton, QTextEdit, QMenuBar, QMenu, QStatusBar)
from src import system, database, data, values, dataTypes, network, ethereum, account, validators, cryptography, threads
from src.GUI import gui_error, gui_userInput, gui_userChoice, gui_message, gui_initMainWindow
from time import gmtime, strftime


class Ui(QMainWindow):
    def __init__(self, dbName):
        try:
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
            self.action_ViewOnlyAccount = QAction(self)
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
            self.comboBox_tokens = QComboBox(self.gridLayoutWidget_tokens)
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
            self.balanceThread = threads.GetBalance()

            self.db = database.SQLITE(dbName)
            # self.transactionResult = {'message': '', 'hash': '', 'pending': 0}
            self.transactionResult = {}

            self.coins = []
            self.initMainWindow = gui_initMainWindow.WINDOW(self)
            self._setEvents()
            self._setNetWork()
            self.setAddress()
            self.getCoinsList()

        except Exception as er:
            system.errorSignal.newError.emit(f"Ui -> __init__ -> {er}")
            exit()

    def _setEvents(self):
        try:
            self.pushButton_copyAddress.clicked.connect(self.copyAddress)
            self.pushButton_etherScan.clicked.connect(self.goToEtherscan)
            self.pushButton_nodeProvider.clicked.connect(self.goToEtherNodes)
            self.pushButton_accountName.clicked.connect(self.editAccountName)
            self.pushButton_deleteAccount.clicked.connect(self.deleteAccount)
            self.pushButton_send.clicked.connect(self.sendERC20Transaction)
            # Wallets-New wallet---------------------------------------------------------------------------------
            self.action_newRandomAccount.triggered.connect(self.createAccountRandom)
            self.action_recoverFromMnemonic.triggered.connect(self.createAccountFromMnemonic)
            self.action_recoverFromEntropy.triggered.connect(self.createAccountFromEntropy)
            self.action_recoverFromPrivateKey.triggered.connect(self.createAccountFromPrivateKey)
            self.action_ViewOnlyAccount.triggered.connect(self.createViewOnlyAccount)
            # Wallets-Secrets-------------------------------------------------------------------------------------
            self.action_entropy.triggered.connect(lambda: self.showSecrets(dataTypes.ACCOUNT.ENTROPY))
            self.action_privateKey.triggered.connect(lambda: self.showSecrets(dataTypes.ACCOUNT.PRIVATE_KEY))
            self.action_publicKeyCoordinates.triggered.connect(lambda: self.showSecrets(dataTypes.ACCOUNT.PUBLIC_KEY_X))
            self.action_publicKey.triggered.connect(lambda: self.showSecrets(dataTypes.ACCOUNT.PUBLIC_KEY))
            self.action_mnemonic.triggered.connect(lambda: self.showSecrets(dataTypes.ACCOUNT.MNEMONIC))
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
            self.radioButton_mainNet.toggled.connect(self.networkChange)
            self.radioButton_testNet.toggled.connect(self.networkChange)
            # -------------------------------------------------------------------------------------------------------
            self.lineEdit_sendValue.textChanged.connect(self.lineEditSendValueChange)
            self.lineEdit_nodeProvider.textChanged.connect(self.lineEditProviderChange)
            self.comboBox_activeAddressVal.currentTextChanged.connect(self.comboBoxAddressChange)
            self.comboBox_tokens.currentTextChanged.connect(self.comboBoxTokenChange)
            self.balanceThread.finished.connect(self.close)
            self.balanceThread.ok.connect(self.ReceiveBalance)

        except Exception as er:
            raise Exception('_setEvents -> ', str(er))

    def setAddress(self):
        try:
            if self.db.isTableEmpty('accounts'):  # there is no account in database
                createAccount_window = gui_userChoice.WINDOW('Create new account', 'There is no account!',
                                                             'Create new one?')
                createAccount_window.exec()
                if not createAccount_window.getAnswer():  # cancel by user
                    gui_message.WINDOW('Create new account', 'You always can create new account or restore old one',
                                       'Wallet -> New account').exec()
                else:  # create first new account
                    acc = account.New.random()  # create new account
                    self.db.insertAccountRow(acc)
                    self.setAddress()  # call itself to add new address in ui elements
            else:
                accounts = self.db.readAllRows(tableName=values.TABLE_ACCOUNT)
                for ac in accounts:
                    self.lineEdit_accountName.setText(str(ac[0]))
                    self.comboBox_activeAddressVal.addItem(ac[1])
                    self.comboBox_activeAddressVal.setCurrentIndex(self.comboBox_activeAddressVal.count() - 1)
        except Exception as er:
            system.errorSignal.newError.emit(f"Ui -> setAddress -> {er}")

    def _setNetWork(self):
        try:
            print(self.comboBox_tokens.currentText())
            if self.comboBox_tokens.currentText() == 'Ethereum':
                pass  # ETH is available in both net
            else:
                if not self.comboBox_tokens.currentText() == values.COMBO_BOX_TOKEN:  # COMBO_BOX_TOKEN = initialize
                    netType = self.db.readColumn(tableName=values.TABLE_TOKEN,
                                                 columnName=dataTypes.TOKEN.TYPE.value,
                                                 condition=dataTypes.TOKEN.NAME.value,
                                                 conditionVal=self.comboBox_tokens.currentText())
                    if netType[0][0] == 'MainNet' or not netType[0][0]:
                        self.radioButton_mainNet.setChecked(True)
                        self.radioButton_testNet.setChecked(False)
                    elif netType[0][0] == 'Sepolia':
                        self.radioButton_mainNet.setChecked(False)
                        self.radioButton_testNet.setChecked(True)
                    else:
                        raise Exception(f"netWork type")
        except Exception as er:
            raise Exception('_setMainNet -> ', str(er))

    def getCoinsList(self):
        try:
            coins = data.readAllFavoriteTokens(self.db)
            for coin in coins:
                self.coins.append({dataTypes.TOKEN.NAME.value: coin[dataTypes.TOKEN.NAME.value],
                                   dataTypes.TOKEN.SYMBOL.value: coin[dataTypes.TOKEN.SYMBOL.value],
                                   dataTypes.TOKEN.TYPE.value: coin[dataTypes.TOKEN.TYPE.value],
                                   dataTypes.TOKEN.ADDRESS.value: coin[dataTypes.TOKEN.ADDRESS.value],
                                   dataTypes.TOKEN.CHAIN_ID.value: coin[dataTypes.TOKEN.CHAIN_ID.value],
                                   dataTypes.TOKEN.LOGO.value: coin[dataTypes.TOKEN.LOGO.value],
                                   dataTypes.TOKEN.ABI.value: coin[dataTypes.TOKEN.ABI.value],
                                   'balance': 0})
            for tok in self.coins:
                self.addNewItemToComboBoxToken(tok)
        except Exception as er:
            system.errorSignal.newError.emit(f"Ui -> getCoinsList -> {er}")

    def addNewItemToComboBoxToken(self, item: dict):
        try:
            self._setNetWork()
            index = self.comboBox_tokens.currentIndex()
            res = network.getRequest(str(item[dataTypes.TOKEN.LOGO.value]))
            pixmap = QPixmap()
            pixmap.loadFromData(res.content)
            self.comboBox_tokens.insertItem(index, item[dataTypes.TOKEN.NAME.value])
            self.comboBox_tokens.setItemIcon(index, QIcon(QIcon(pixmap)))
            self.comboBox_tokens.setIconSize(QSize(values.ICON_SIZE, values.ICON_SIZE))
            self.comboBox_tokens.setCurrentIndex(index)
            self.comboBox_tokens.removeItem(self.comboBox_tokens.findText(values.COMBO_BOX_TOKEN))
            self.setLabelAmountValStyleSheet(item[dataTypes.TOKEN.SYMBOL.value], float(item['balance']), 'red')
        except Exception as er:
            system.errorSignal.newError.emit(f"Ui -> addNewItemToComboBoxToken -> {er}")

    def setLabelAmountValStyleSheet(self, symbol: str, balance: float, color: str):
        try:
            self.label_amountVal.setText(
                f"<span style = 'color: {color}; font-weight: bold;' > {balance}"
                f"</ span> <span style = 'color: rgb(140, 170, 250); font-weight: bold;' >"
                f" {symbol} </ span>")
        except Exception as er:
            system.errorSignal.newError.emit(f"Ui -> setLabelAmountValStyleSheet -> {er}")

    def ReceiveBalance(self, balance, symbol):
        try:
            if balance < 0:
                # error in getting balance
                self.statusbar.showMessage(f"negative balance ! something is wrong")
            else:
                color = 'red'
                if balance > 0:
                    color = 'green'
                self.setLabelAmountValStyleSheet(symbol, float(balance), color)
                self.resetStatueBarStyleSheet()
                print(f"{strftime('%H:%M:%S', gmtime())}: {symbol} balance = {balance}")
        except Exception as er:
            print(f"{strftime('%H:%M:%S', gmtime())}: UI -> ReceiveBalance:{symbol} -> {er} ")

    def resetStatueBarStyleSheet(self):
        try:
            self.statusbar.clearMessage()
            statusbarStyle = (
                "background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,"
                "stop:0 rgb(30, 76, 108) , stop:1 rgb(47, 54, 60)); color: white;"
            )
            self.statusbar.setStyleSheet(statusbarStyle)
        except Exception as er:
            system.errorSignal.newError.emit(f"Ui -> resetStatueBarStyleSheet -> {er}")

    def comboBoxTokenChange(self):
        try:
            self._setNetWork()

            def error(msg):
                self.statusbar.setStyleSheet("background-color: red; color: white")
                self.statusbar.showMessage(f"balance is not synchronized. \n{msg}")

            if not self.comboBox_activeAddressVal.count() == 0:  # 0 means no account available
                self.setLabelAmountValStyleSheet('None', 0, 'White')  # reset and wait to get balance
                if self.balanceThread.isRunning():
                    pass  # nothing to do
                    # self.balanceThread.quit()
                    # self.balanceThread.exit()
                    # self.balanceThread.terminate()
                for coin in self.coins:
                    if self.comboBox_tokens.currentText() == coin[dataTypes.TOKEN.NAME.value]:
                        coinData = {
                            'provider': self.lineEdit_nodeProvider.text(),
                            'activeAddress': self.comboBox_activeAddressVal.currentText(),
                            'coinsData': [
                                coin[dataTypes.TOKEN.NAME.value],
                                coin[dataTypes.TOKEN.SYMBOL.value],
                                coin[dataTypes.TOKEN.ADDRESS.value]
                            ]
                        }
                        self.balanceThread.setCoin(coinData)
                        # print('is signal connect')
                        # print(self.balanceThread.isSignalConnected(self.balanceThread.error))
                        # if not self.balanceThread.isSignalConnected(self.balanceThread.error):
                        self.balanceThread.error.connect(error)
                        if not self.balanceThread.isRunning():
                            self.balanceThread.start()
                        self.resetStatueBarStyleSheet()
                    else:
                        pass  # to continue
                        # raise Exception(f"'{coin[dataTypes.TOKEN.NAME.value]}' is not in main list")
        except Exception as er:
            self.statusbar.setStyleSheet("background-color: red; color: white")
            self.statusbar.showMessage(f"balance is not synchronized. \n{er}")

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
            print(f"{strftime('%H:%M:%S', gmtime())}: {er}")

    def networkChange(self):
        try:
            if self.radioButton_mainNet.isChecked() and not self.radioButton_testNet.isChecked():
                self.lineEdit_nodeProvider.setText(values.ETHEREUM_PROVIDER)
            elif not self.radioButton_mainNet.isChecked() and self.radioButton_testNet.isChecked():
                self.lineEdit_nodeProvider.setText(values.SEPOLIA_PROVIDER)
            else:
                raise Exception("unknown network status")
            self.comboBox_tokens.currentTextChanged.emit('')  # send signal to run function
        except Exception as er:
            system.errorSignal.newError.emit(f"Ui -> networkChange -> {er}")

    def comboBoxAddressChange(self):
        try:
            if self.comboBox_activeAddressVal.count() == 0:
                self.lineEdit_accountName.clear()
                self.setLabelAmountValStyleSheet('None', 0, 'White')
            else:
                name = self.db.readColumn(tableName=values.TABLE_ACCOUNT,
                                          columnName=dataTypes.ACCOUNT.NAME.value,
                                          condition=dataTypes.ACCOUNT.ADDRESS.value,
                                          conditionVal=self.comboBox_activeAddressVal.currentText())[0][0]
                self.lineEdit_accountName.setText(name)
                self.setLabelAmountValStyleSheet('None', 0, 'White')  # reset and wait to get balance
                self.comboBox_tokens.currentTextChanged.emit('')  # send signal to run function
        except Exception as er:
            system.errorSignal.newError.emit(f"Ui -> comboBoxAddressChange -> {er}")

    def lineEditProviderChange(self):
        try:
            self.comboBox_tokens.currentTextChanged.emit('')
        except Exception as er:
            system.errorSignal.newError.emit(f"Ui -> lineEditProviderChange -> {er}")

    def editAccountName(self):
        try:
            if self.pushButton_accountName.text() == 'Edit':
                self.lineEdit_accountName.setEnabled(True)
                self.lineEdit_accountName.setStyleSheet("background-color: rgb(250, 240, 200); color: black")
                self.pushButton_accountName.setText('Save')
                self.pushButton_accountName.setIcon(QIcon(system.getIconPath('save.png')))
                self.pushButton_nodeProvider.setIconSize(QSize(values.ICON_SIZE, values.ICON_SIZE))
            elif self.pushButton_accountName.text() == 'Save':
                self.lineEdit_accountName.setEnabled(False)
                self.lineEdit_accountName.setStyleSheet(
                    "background-color: transparent; border: none;"
                    "color: rgb(108, 204, 244); font-weight: bold;")
                self.pushButton_accountName.setText('Edit')
                self.pushButton_accountName.setIcon(QIcon(system.getIconPath('edit.png')))
                self.pushButton_nodeProvider.setIconSize(QSize(values.ICON_SIZE, values.ICON_SIZE))
                self.db.updateRowColumnValue('accounts', 'NAM',
                                             self.lineEdit_accountName.text(), 'ADR',
                                             self.comboBox_activeAddressVal.currentText())
        except Exception as er:
            system.errorSignal.newError.emit(f"Ui -> editAccountName -> {er}")

    def createAccountRandom(self):
        try:
            userAnswer = True
            doIt = True
            if self.db.isTableEmpty(tableName=values.TABLE_ACCOUNT):
                createAccount_window = gui_userChoice.WINDOW('Create new random account',
                                                             'Some account(s) already exist',
                                                             'Create new one?')
                createAccount_window.exec()
                userAnswer = createAccount_window.getAnswer()
            if not userAnswer:
                doIt = False  # cancel by user
            if doIt:
                acc = account.New.random()  # create new account
                self.db.insertAccountRow(acc)
                self.lineEdit_accountName.setText(acc['name'])
                self.comboBox_activeAddressVal.addItem(acc['address'])
                self.comboBox_activeAddressVal.setCurrentIndex(self.comboBox_activeAddressVal.count() - 1)
        except Exception as er:
            system.errorSignal.newError.emit(f"Ui -> createAccountRandom -> {er}")

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
                self.db.insertAccountRow(acc)
                self.lineEdit_accountName.setText(acc['name'])
                self.comboBox_activeAddressVal.addItem(acc['address'])
                self.comboBox_activeAddressVal.setCurrentIndex(self.comboBox_activeAddressVal.count() - 1)
        except Exception as er:
            system.errorSignal.newError.emit(f"Ui -> createAccountFromEntropy -> {er}")

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
                self.lineEdit_accountName.setText(acc['name'])
                self.comboBox_activeAddressVal.addItem(acc['address'])
                self.comboBox_activeAddressVal.setCurrentIndex(self.comboBox_activeAddressVal.count() - 1)
        except Exception as er:
            system.errorSignal.newError.emit(f"Ui -> createAccountFromPrivateKey -> {er}")

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
                self.lineEdit_accountName.setText(acc['name'])
                self.comboBox_activeAddressVal.addItem(acc['address'])
                self.comboBox_activeAddressVal.setCurrentIndex(self.comboBox_activeAddressVal.count() - 1)
        except Exception as er:
            system.errorSignal.newError.emit(f"Ui -> createAccountFromMnemonic -> {er}")

    def createViewOnlyAccount(self):
        try:
            getAddress = gui_userInput.WINDOW('View Only Account',
                                              'Enter target address:')
            getAddress.exec()
            address = getAddress.getInput()
            if address:
                validators.checkHex(address)
                acc = {'entropy': '',
                       'privateKey': '',
                       'publicKeyCoordinate': ('', ''),
                       'publicKey': '',
                       'address': address,
                       'mnemonic': '',
                       'name': 'No name'}
                self.db.insertAccountRow(acc)
                self.comboBox_activeAddressVal.addItem(acc['address'])
                self.comboBox_activeAddressVal.setCurrentIndex(self.comboBox_activeAddressVal.count() - 1)
        except Exception as er:
            system.errorSignal.newError.emit(f"Ui -> createViewOnlyAccount -> {er}")

    def goToEtherscan(self):
        try:
            active_address = self.comboBox_activeAddressVal.currentText()
            if active_address is None:
                gui_message.WINDOW('goToEtherscan', 'No address selected').exec()
            else:
                if self.radioButton_mainNet.isChecked() and not self.radioButton_testNet.isChecked():
                    self.webEngineView.setUrl(QUrl(f"{values.ETH_SCAN_PRE}{active_address}"))
                    self.tabWidget_main.setCurrentIndex(4)
                elif not self.radioButton_mainNet.isChecked() and self.radioButton_testNet.isChecked():
                    self.webEngineView.setUrl(QUrl(f"{values.SEPOLIA_SCAN_PRE}{active_address}"))
                    self.tabWidget_main.setCurrentIndex(4)
                else:
                    raise Exception("unknown network status")
        except Exception as er:
            system.errorSignal.newError.emit(f"Ui -> goToEtherscan -> {er}")

    def goToEtherNodes(self):
        try:
            if self.radioButton_mainNet.isChecked() and not self.radioButton_testNet.isChecked():
                self.webEngineView.setUrl(QUrl(values.ETHEREUM_NOD_URI))
                self.tabWidget_main.setCurrentIndex(4)
            elif not self.radioButton_mainNet.isChecked() and self.radioButton_testNet.isChecked():
                self.webEngineView.setUrl(QUrl(values.SEPOLIA_NOD_URI))
                self.tabWidget_main.setCurrentIndex(4)
            else:
                raise Exception("unknown network status")
        except Exception as er:
            system.errorSignal.newError.emit(f"Ui -> goToEtherNodes -> {er}")

    def copyAddress(self):
        try:
            active_address = self.comboBox_activeAddressVal.currentText()
            if active_address is not None:
                copy(active_address)
            # spam = pyperclip.paste()
        except Exception as er:
            system.errorSignal.newError.emit(f"Ui -> copyAddress -> {er}")

    def showSecrets(self, secretType: dataTypes.ACCOUNT):
        try:
            if not self.db.readColumn(values.TABLE_ACCOUNT,
                                      dataTypes.ACCOUNT.PRIVATE_KEY.value, dataTypes.ACCOUNT.ADDRESS.value,
                                      self.comboBox_activeAddressVal.currentText())[0][0]:
                gui_message.WINDOW("Show secrets", "View only account",
                                   "no secret can be retrieved").exec()
            else:
                self.textEdit_main.clear()
                if secretType == dataTypes.ACCOUNT.ENTROPY and (
                        self.db.readColumn(
                            tableName=values.TABLE_ACCOUNT,
                            columnName=dataTypes.ACCOUNT.ENTROPY.value,
                            condition=dataTypes.ACCOUNT.ADDRESS.value,
                            conditionVal=self.comboBox_activeAddressVal.currentText()
                        ) == self.db.readColumn(
                    tableName=values.TABLE_ACCOUNT,
                    columnName=dataTypes.ACCOUNT.PRIVATE_KEY.value,
                    condition=dataTypes.ACCOUNT.ADDRESS.value,
                    conditionVal=self.comboBox_activeAddressVal.currentText())):
                    gui_message.WINDOW('Show secrets',
                                       'You have recovered an old account.',
                                       'Entropy is not recoverable from private key').exec()
                elif secretType == dataTypes.ACCOUNT.MNEMONIC and (
                        self.db.readColumn(
                            tableName=values.TABLE_ACCOUNT,
                            columnName=dataTypes.ACCOUNT.MNEMONIC.value,
                            condition=dataTypes.ACCOUNT.ADDRESS.value,
                            conditionVal=self.comboBox_activeAddressVal.currentText()
                        ) == self.db.readColumn(
                    tableName=values.TABLE_ACCOUNT,
                    columnName=dataTypes.ACCOUNT.PRIVATE_KEY.value,
                    condition=dataTypes.ACCOUNT.ADDRESS.value,
                    conditionVal=self.comboBox_activeAddressVal.currentText())):
                    gui_message.WINDOW('Show secrets',
                                       'You have recovered an old account.',
                                       'Mnemonic is not recoverable from private key').exec()
                elif secretType == dataTypes.ACCOUNT.PUBLIC_KEY_X or secretType == dataTypes.ACCOUNT.PUBLIC_KEY_Y:
                    result_X = self.db.readColumn(
                        tableName=values.TABLE_ACCOUNT,
                        columnName=dataTypes.ACCOUNT.PUBLIC_KEY_X.value,
                        condition=dataTypes.ACCOUNT.ADDRESS.value,
                        conditionVal=self.comboBox_activeAddressVal.currentText())
                    result_Y = self.db.readColumn(
                        tableName=values.TABLE_ACCOUNT,
                        columnName=dataTypes.ACCOUNT.PUBLIC_KEY_Y.value,
                        condition=dataTypes.ACCOUNT.ADDRESS.value,
                        conditionVal=self.comboBox_activeAddressVal.currentText())
                    if len(result_X) == 1 and len(result_Y) == 1:
                        self.textEdit_main.append(f'Your account PUBLIC_KEY COORDINATE keep it safe:\n')
                        self.textEdit_main.append('X : ' + result_X[0][0])
                        self.textEdit_main.append('Y : ' + result_Y[0][0])
                    else:
                        raise Exception(f"failed to receive coordinates from database.\nX: {result_X}\nY: {result_Y}")
                else:
                    result = self.db.readColumn(
                        tableName=values.TABLE_ACCOUNT,
                        columnName=secretType.value,
                        condition=dataTypes.ACCOUNT.ADDRESS.value,
                        conditionVal=self.comboBox_activeAddressVal.currentText())
                    if len(result) == 1:
                        self.textEdit_main.append(f'Your account {secretType.name} keep it safe:\n')
                        self.textEdit_main.append(f'{result[0][0]}\n')
                        if secretType == dataTypes.ACCOUNT.MNEMONIC or secretType == dataTypes.ACCOUNT.ENTROPY:
                            self.textEdit_main.append(f'{secretType.name} + Passphrase = your account\n\n'
                                                      f'{secretType.name} without Passphrase = unknown account\n'
                                                      f'(If no passphrase set = your account)')
                        elif secretType == dataTypes.ACCOUNT.PRIVATE_KEY:
                            self.textEdit_main.append(f'{secretType.name} = your account')
                    else:
                        raise Exception(f"failed to receive {secretType.name} from database.")
        except Exception as er:
            system.errorSignal.newError.emit(f"Ui -> showSecrets -> {er}")

    def _transactionElements(self, txData: str = ''):
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
                validators.checkURI(self.lineEdit_nodeProvider.text())
                print(f"{strftime('%H:%M:%S', gmtime())}: chainId = {chainId}")
                return {
                    'sender': self.comboBox_activeAddressVal.currentText(),
                    'receiver': to,
                    'vale': val,
                    'provider': self.lineEdit_nodeProvider.text(),
                    'chainId': chainId,
                    'data': txData
                }
            else:
                raise Exception("selecting main or test net")
        except Exception as er:
            raise Exception('transactionElements -> ', str(er))

    def _setPriority(self, transactions, gas) -> dict:
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
            raise Exception('setPriority -> ', str(er))

    def _showTransaction(self, txHash):
        try:
            validators.checkURI(self.lineEdit_nodeProvider.text())
            validators.checkHex(txHash)
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

    def sendERC20Transaction(self, duplicate: bool = False):
        try:
            if not self.lineEdit_message.text() and not self.lineEdit_sendValue.text():
                raise Exception(f"sending options are empty")

            if self.comboBox_tokens.currentText() == 'Ethereum':
                if self.lineEdit_message.text():
                    self._sentMessage(duplicate)
                elif not self.lineEdit_message.text() and self.lineEdit_sendValue.text():
                    self._sentETH(duplicate)
            else:
                self._sendToken(duplicate)
            if self.transactionResult:
                self.textEdit_main.clear()
                self.textEdit_main.setText(f"{self.transactionResult}")
                if self.transactionResult['message'] == 'succeed':
                    gui_message.WINDOW("Your job is done', 'Transaction succeed:",
                                       f"Hash: {self.transactionResult['hash']}").exec()
                    self._showTransaction(self.transactionResult['hash'])
                    cursor = QTextCursor(self.textEdit_main.document())
                    cursor.setPosition(0)
                    self.textEdit_main.setTextCursor(cursor)
                    self.textEdit_main.insertPlainText(f"transaction Hash:\n{self.transactionResult['hash']}\n"
                                                       f"--------------------\n")
                    self.lineEdit_sendValue.clear()
                    self.lineEdit_message.clear()
                    self.lineEdit_sendAddress.clear()
        except Exception as er:
            system.errorSignal.newError.emit(f"Ui -> send -> {er}")
            if self.transactionResult:
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
                        self.sendERC20Transaction(True)

    def _sendToken(self, duplicate):
        try:
            if not self.lineEdit_sendAddress.text():
                raise Exception(f"address = '{self.lineEdit_sendAddress.text()}' !")

            if not self.lineEdit_sendValue.text():
                raise Exception(f"value = '{self.lineEdit_sendValue.text()}' !")
            token = self.comboBox_tokens.currentText()
            transactions = self._transactionElements()
            contractAddress, abi, chainID = data.getTokenInfo(self.coins, token)
            transactions['chainId'] = chainID
            transactions['abi'] = abi
            transactions['contractAddress'] = contractAddress
            # transactions['sender'] = self.comboBox_activeAddressVal.currentText()

            # gas = ethereum.estimateGas(transactions)
            gas = {   # should be found in the better way
                'MAXPriorityFee':
                {
                    'low': Decimal('0.550000'),
                    'medium': Decimal('0.750000'),
                    'high': Decimal('0.950000')
                },
                'MAX_Fee':
                    {
                        'low': Decimal('0.750000'),
                        'medium': Decimal('0.950000'),
                        'high': Decimal('1.150000')
                    },
                'GasPrice':
                    {
                        'low': Decimal('0.000200'),
                        'medium': Decimal('0.000250'),
                        'high': Decimal('0.000350')
                    }
            }

            senToken = gui_userChoice.WINDOW('Sending your money to others',
                                             f"Send: {transactions['vale']} {token}\n"
                                             f"to: '{transactions['receiver']}'\n"
                                             f"estimated gas fee is:\n"
                                             f"Lowest: {gas['GasPrice']['low']} ETH\n"
                                             f"Median: {gas['GasPrice']['medium']} ETH\n"
                                             f"Highest: {gas['GasPrice']['high']} ETH\n",
                                             'Are you sure?')
            senToken.exec()
            if not senToken.getAnswer():  # cancel by user
                gui_message.WINDOW('I\'m entranced with joy', 'You are in safe',
                                   'Nothing has been sent').exec()
            else:
                transactions = self._setPriority(transactions, gas)
                transactionResult = ethereum.sendTokenTransaction(
                    privateKey=(self.db.readColumn('accounts',
                                                   dataTypes.ACCOUNT.PRIVATE_KEY.value, 'ADR',
                                                   transactions['sender']))[0][0],
                    txElements=transactions,
                    duplicate=duplicate)
                self.transactionResult = transactionResult
                if self.transactionResult['message'] != 'succeed':
                    raise Exception(f"{self.transactionResult['message']}")
        except Exception as er:
            raise Exception(f"_sendToken -> {er}")

    def _sentETH(self, duplicate: bool = False):
        try:
            if not self.lineEdit_sendAddress.text():
                raise Exception(f"address = '{self.lineEdit_sendAddress.text()}' !")

            if not self.lineEdit_sendValue.text():
                raise Exception(f"value = '{self.lineEdit_sendValue.text()}' !")

            transactions = self._transactionElements()
            gas = ethereum.estimateGas(transactions)
            print(gas)
            print('=' * 20)
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
                transactions = self._setPriority(transactions, gas)
                transactionResult = ethereum.sendValueTransaction(
                    privateKey=(self.db.readColumn('accounts',
                                                   dataTypes.ACCOUNT.PRIVATE_KEY.value, 'ADR',
                                                   transactions['sender']))[0][0],
                    txElements=transactions,
                    duplicate=duplicate)
                self.transactionResult = transactionResult
                if self.transactionResult['message'] != 'succeed':
                    raise Exception(f"{self.transactionResult['message']}")
        except Exception as er:
            raise Exception(f"_sentETH -> {er}")

    def _sentMessage(self, duplicate: bool = False):
        try:
            if not self.lineEdit_sendAddress.text():
                raise Exception(f"address = '{self.lineEdit_sendAddress.text()}' !")

            if not self.lineEdit_message.text():
                raise Exception(f"message = '{self.lineEdit_sendValue.text()}' !")
            message = self.lineEdit_message.text()

            transactions = self._transactionElements(txData=message.encode("utf-8").hex())
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
                transactions = self._setPriority(transactions, gas)
                transactionResult = ethereum.sendMessageTransaction(
                    privateKey=(self.db.readColumn('accounts',
                                                   dataTypes.ACCOUNT.PRIVATE_KEY.value, 'ADR',
                                                   transactions['sender']))[0][0],
                    txElements=transactions,
                    duplicate=duplicate)
                self.transactionResult = transactionResult
                if self.transactionResult['message'] != 'succeed':
                    raise Exception(f"{self.transactionResult['message']}")
        except Exception as er:
            raise Exception(f"_sentMessage -> {er}")

    def showTransactionMessage(self, txHash):
        try:
            validators.checkURI(self.lineEdit_nodeProvider.text())
            validators.checkHex(txHash)
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
            system.errorSignal.newError.emit(f"Ui -> showTransactionMessage -> {er}")

    def showCustomTransaction(self):
        try:
            TXHashWindow = gui_userInput.WINDOW('Show custom transaction',
                                                'Enter transaction hash:\n'
                                                '(Notice about mainNet and testNet)')
            TXHashWindow.exec()
            TXHash = TXHashWindow.getInput()
            if TXHash:
                validators.checkHex(TXHash)
                self._showTransaction(TXHash)
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
                validators.checkHex(TXHash)
                self.showTransactionMessage(TXHash)
        except Exception as er:
            gui_error.WINDOW('showCustomTransactionMessage', str(er)).exec()

    def showNonce(self):
        try:
            validators.checkURI(self.lineEdit_nodeProvider.text())
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
            validators.checkURI(self.lineEdit_nodeProvider.text())
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
                validators.checkHex(TxHash)
                validators.checkURI(self.lineEdit_nodeProvider.text())
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
            rowData = self.db.readRow('accounts', 'ADR',
                                      self.comboBox_activeAddressVal.currentText())[0]
            data = {'entropy': rowData[0],
                    'privateKey': rowData[1],
                    'publicKeyCoordinate': (rowData[2], rowData[3]),
                    'publicKey': rowData[4],
                    'address': rowData[5],
                    'mnemonic': rowData[6],
                    'name': rowData[7]}
            root = Tk()
            root.withdraw()
            selectedFolder = filedialog.askdirectory()
            if selectedFolder:
                passwordWindow = gui_userInput.WINDOW('backupWallet',
                                                      'Exporting the secrets of your account to the file.\n'
                                                      'For more security set a password on the file\n'
                                                      'or cancel for skip password protection')
                passwordWindow.exec()
                password = passwordWindow.getInput()
                if password:
                    fileName = (f"{selectedFolder}/{rowData[7].replace(' ', '_')}-"
                                f"{rowData[5][2:5]}-{rowData[5][-3:]}"
                                f".wallet")
                    b_password = password.encode('utf-8')
                    b_data = dumps(data, indent=2).encode('utf-8')
                    dataToWrite = cryptography.AES.encrypt(b_password, b_data)
                else:
                    fileName = (f"{selectedFolder}/{rowData[7].replace(' ', '_')}-"
                                f"{rowData[5][2:5]}-{rowData[5][-3:]}"
                                f".json")
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
            else:
                pass  # no folder selected
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
                        decrypted = cryptography.AES.decrypt(password.encode('utf-8'), data)
                        jsonData = loads(decrypted.decode('utf-8'))
                else:
                    raise Exception(f"unknown file format")
                self.showWallet(jsonData, filePath)
                self.db.insertAccountRow(jsonData)
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
                self.db.deleteRow('accounts', 'ADR', accountToDelete)
                if self.comboBox_activeAddressVal.count() == 1:
                    self.comboBox_activeAddressVal.clear()
                else:
                    self.comboBox_activeAddressVal.removeItem(accountIndex)
                self.textEdit_main.clear()
                gui_message.WINDOW('deleteAccount', 'the account was deleted.').exec()
        except Exception as er:
            gui_error.WINDOW('deleteAccount', str(er)).exec()

    def showPendingTransactions(self):
        pendingBlock = ethereum.getPendingTransactions(self.lineEdit_nodeProvider.text())
        print()
