from PyQt6.QtWidgets import QFrame, QTabWidget
from PyQt6.QtCore import QSize, QRect, QUrl
from PyQt6.QtGui import QIcon
from src import system, database, data, values, dataTypes, network, ethereum, account, validators, cryptography


class WINDOW:
    def __init__(self, parent):
        try:
            self.window = parent
            self.initUI()
            self.initIcons()
            self.initStyleSheet()
        except Exception as er:
            raise Exception(f"gui_initMainWindow -> __init__ -> {er}")

    def initUI(self):
        try:
            self.window.centralWidget_main.setObjectName("centralWidget_main")
            self.window.setCentralWidget(self.window.centralWidget_main)
            self.window.resize(values.MAIN_WINDOW_WIDTH, values.MAIN_WINDOW_HEIGHT)
            self.window.setFixedSize(values.MAIN_WINDOW_WIDTH, values.MAIN_WINDOW_HEIGHT)
            self.window.setObjectName("MainWindow")
            self.window.setWindowTitle("FAwallet")
            self.window.tabWidget_main.setObjectName("tabWidget_main")
            self.window.tabWidget_main.setGeometry(QRect(0, 0, values.MAIN_WINDOW_WIDTH - values.SIDE_TAB_WIDTH,
                                                         values.MAIN_WINDOW_HEIGHT))
            self.window.setMenuBar(self.window.menubar_file)
            # menubar -------------------------------------------------------------------------
            self.window.action_entropy.setObjectName("actionEntropy")
            self.window.action_privateKey.setObjectName("actionPrivateKey")
            self.window.action_publicKeyCoordinates.setObjectName("actionPublicKey_coordinates")
            self.window.action_publicKey.setObjectName("actionPublicKey")
            self.window.action_mnemonic.setObjectName("actionMnemonic")

            self.window.action_newRandomAccount.setObjectName("actionNewRandomAccount")
            self.window.action_recoverFromMnemonic.setObjectName("actionRecover_from_mnemonic")
            self.window.action_recoverFromEntropy.setObjectName("actionRecover_from_entropy")
            self.window.action_recoverFromPrivateKey.setObjectName("actionRecover_from_privateKey")
            self.window.action_ViewOnlyAccount.setObjectName("action_ViewOnlyAccount")
            # ----------------------------------------------------------------------------------
            self.window.action_checkTx.setObjectName("action_checkTX")
            self.window.action_txNonce.setObjectName("actionTX_nonce")
            self.window.action_simpleHistory.setObjectName("actionSimple_history")
            self.window.action_allNormal.setObjectName("actionAll_normal")
            self.window.action_allInternal.setObjectName("actionAll_internal")

            self.window.action_publicKeyFromTxHash.setObjectName("actionPublicKey_from_TXHash")
            self.window.action_transactionMessage.setObjectName('actionTransactionMessage')
            self.window.action_pendingTransactions.setObjectName('action_pendingTransactions ')
            # ----------------------------------------------------------------------------------
            self.window.menubar_file.setObjectName("menubar_file")
            self.window.menubar_file.setGeometry(QRect(0, 0, values.MAIN_WINDOW_WIDTH - values.SIDE_TAB_WIDTH, 25))
            # ----------------------------------------------------------------------------------
            # wallet menu
            self.window.menubar_file.addAction(self.window.menu_wallet.menuAction())
            self.window.menu_wallet.setObjectName("menu_Wallet")
            self.window.menu_wallet.setTitle("&Wallet")

            #  wallet menu -> account menu
            self.window.menu_wallet.addAction(self.window.menu_newAccount.menuAction())
            self.window.menu_newAccount.setObjectName("menuNew_account")
            self.window.menu_newAccount.setTitle("New account")
            self.window.menu_newAccount.addAction(self.window.action_newRandomAccount)
            self.window.action_newRandomAccount.setText("New random account")
            self.window.menu_newAccount.addAction(self.window.action_recoverFromMnemonic)
            self.window.action_recoverFromMnemonic.setText("Recover from mnemonic")
            self.window.menu_newAccount.addAction(self.window.action_recoverFromEntropy)
            self.window.action_recoverFromEntropy.setText("Recover from entropy")
            self.window.menu_newAccount.addAction(self.window.action_recoverFromPrivateKey)
            self.window.action_recoverFromPrivateKey.setText("Recover from privateKey")
            self.window.menu_newAccount.addAction(self.window.action_ViewOnlyAccount)
            self.window.action_ViewOnlyAccount.setText("View only account")

            #  wallet menu -> Secrets menu
            self.window.menu_wallet.addAction(self.window.menu_secrets.menuAction())
            self.window.menu_secrets.setObjectName("menuSecrets")
            self.window.menu_secrets.setTitle("Secrets")
            self.window.menu_secrets.addAction(self.window.action_entropy)
            self.window.action_entropy.setText("Entropy")
            self.window.menu_secrets.addAction(self.window.action_privateKey)
            self.window.action_privateKey.setText("PrivateKey")
            self.window.menu_secrets.addAction(self.window.action_publicKeyCoordinates)
            self.window.action_publicKeyCoordinates.setText("PublicKey coordinates")
            self.window.menu_secrets.addAction(self.window.action_publicKey)
            self.window.action_publicKey.setText('PublicKey')
            self.window.menu_secrets.addAction(self.window.action_mnemonic)
            self.window.action_mnemonic.setText("Mnemonic")

            #  wallet menu -> Backup and restore menu
            self.window.menu_wallet.addAction(self.window.menu_backupAndRestore.menuAction())
            self.window.menu_backupAndRestore.setObjectName("menuBackupAndRestore")
            self.window.menu_backupAndRestore.setTitle("Backup and Restore")
            self.window.menu_backupAndRestore.addAction(self.window.action_backup)
            self.window.action_backup.setText("Backup account")
            self.window.menu_backupAndRestore.addAction(self.window.action_restore)
            self.window.action_restore.setText('Restore account')

            # ----------------------------------------------------------------------------------
            # Network menu
            self.window.menubar_file.addAction(self.window.menu_network.menuAction())
            self.window.menu_network.setObjectName("menu_network")
            self.window.menu_network.setTitle("&Network")

            # Network menu -> Transactions menu
            self.window.menu_network.addAction(self.window.menu_transactions.menuAction())
            self.window.menu_transactions.setObjectName("menu_transactions")
            self.window.menu_transactions.setTitle("Transactions")
            self.window.menu_transactions.addAction(self.window.action_checkTx)
            self.window.action_checkTx.setText("Check transaction")
            self.window.menu_transactions.addAction(self.window.action_txNonce)
            self.window.action_txNonce.setText("Transaction nounce")
            self.window.menu_transactions.addAction(self.window.action_simpleHistory)
            self.window.action_simpleHistory.setText("Simple history(need APIkey)")
            self.window.menu_transactions.addAction(self.window.action_allNormal)
            self.window.action_allNormal.setText("All normal TXS (need APIkey)")
            self.window.menu_transactions.addAction(self.window.action_allInternal)
            self.window.action_allInternal.setText("All internal TXS (need APIkey)")

            # Network menu -> Tools menu
            self.window.menu_network.addAction(self.window.menu_tools.menuAction())
            self.window.menu_tools.setObjectName("menu_tools")
            self.window.menu_tools.setTitle("Tools")
            self.window.menu_tools.addAction(self.window.action_publicKeyFromTxHash)
            self.window.action_publicKeyFromTxHash.setText("PublicKey from TXHash")
            self.window.menu_tools.addAction(self.window.action_transactionMessage)
            self.window.action_transactionMessage.setText('Show transaction message')
            self.window.menu_tools.addAction(self.window.action_pendingTransactions)
            self.window.action_pendingTransactions.setText('pending transactions')
            # ----------------------------------------------------------------------------------
            self.window.tabWidget_main.setTabPosition(QTabWidget.TabPosition.West)
            #  tabs  ---------------------------------------------------------------------------
            #  tab accounts
            self.window.tabWidget_main.addTab(self.window.tab_accounts, "Accounts")
            self.window.tab_accounts.setObjectName("tab_accounts")
            self.window.gridLayoutWidget_accounts.setObjectName("gridLayoutWidget_accounts")
            self.window.gridLayoutWidget_accounts.setGeometry(QRect(
                0, 0, values.MAIN_WINDOW_WIDTH - (2 * values.SIDE_TAB_WIDTH),
                values.MAIN_WINDOW_HEIGHT - values.GUI_ITEM_HEIGHT - values.GUI_MENU_HEIGHT))
            self.window.gridlayout_accounts.setObjectName("gridlayout_accounts")
            self.window.gridlayout_accounts.setGeometry(QRect(
                0, 0, values.MAIN_WINDOW_WIDTH - (2 * values.SIDE_TAB_WIDTH),
                values.MAIN_WINDOW_HEIGHT - values.GUI_ITEM_HEIGHT - values.GUI_MENU_HEIGHT))

            #  tab tokens
            self.window.tabWidget_main.addTab(self.window.tab_tokens, "Tokens")
            self.window.tab_tokens.setObjectName("tab_tokens")
            self.window.gridLayoutWidget_tokens.setObjectName("gridLayoutWidget_tokens")
            self.window.gridLayoutWidget_tokens.setGeometry(QRect(
                0, 0, values.MAIN_WINDOW_WIDTH - (2 * values.SIDE_TAB_WIDTH),
                values.MAIN_WINDOW_HEIGHT - values.GUI_ITEM_HEIGHT - values.GUI_MENU_HEIGHT))
            self.window.gridlayout_tokens.setObjectName("gridlayout_tokens")
            self.window.gridlayout_tokens.setGeometry(QRect(
                0, 0, values.MAIN_WINDOW_WIDTH - (2 * values.SIDE_TAB_WIDTH),
                values.MAIN_WINDOW_HEIGHT - values.GUI_ITEM_HEIGHT - values.GUI_MENU_HEIGHT))

            # tab contract
            self.window.tabWidget_main.addTab(self.window.tab_contract, "Contract")
            self.window.tab_contract.setObjectName("tab_contract")
            self.window.gridLayoutWidget_contract.setObjectName("gridLayoutWidget_contract")
            self.window.gridLayoutWidget_contract.setGeometry(QRect(
                0, 0, values.MAIN_WINDOW_WIDTH - (2 * values.SIDE_TAB_WIDTH),
                values.MAIN_WINDOW_HEIGHT - values.GUI_ITEM_HEIGHT - values.GUI_MENU_HEIGHT))
            self.window.gridlayout_contract.setObjectName("gridlayout_contract")
            self.window.gridlayout_contract.setGeometry(QRect(
                0, 0, values.MAIN_WINDOW_WIDTH - (2 * values.SIDE_TAB_WIDTH),
                values.MAIN_WINDOW_HEIGHT - values.GUI_ITEM_HEIGHT - values.GUI_MENU_HEIGHT))

            # tab nft
            self.window.tabWidget_main.addTab(self.window.tab_nft, "NFT")
            self.window.tab_nft.setObjectName("tab_nft")
            self.window.gridLayoutWidget_nft.setObjectName("gridLayoutWidget_nft")
            self.window.gridLayoutWidget_nft.setGeometry(QRect(
                0, 0, values.MAIN_WINDOW_WIDTH - (2 * values.SIDE_TAB_WIDTH),
                values.MAIN_WINDOW_HEIGHT - values.GUI_ITEM_HEIGHT - values.GUI_MENU_HEIGHT))
            self.window.gridlayout_nft.setObjectName("gridlayout_nft")
            self.window.gridlayout_nft.setGeometry(QRect(
                0, 0, values.MAIN_WINDOW_WIDTH - (2 * values.SIDE_TAB_WIDTH),
                values.MAIN_WINDOW_HEIGHT - values.GUI_ITEM_HEIGHT - values.GUI_MENU_HEIGHT))

            # tab webView
            self.window.tabWidget_main.addTab(self.window.tab_webView, "WebView")
            self.window.tab_webView.setObjectName("tab_webView")
            self.window.gridLayoutWidget_webView.setObjectName("gridLayoutWidget_webView")
            self.window.gridLayoutWidget_webView.setGeometry(QRect(
                0, 0, values.MAIN_WINDOW_WIDTH - (2 * values.SIDE_TAB_WIDTH),
                values.MAIN_WINDOW_HEIGHT - values.GUI_ITEM_HEIGHT - values.GUI_MENU_HEIGHT))
            self.window.gridlayout_webView.setObjectName("gridlayout_webView")
            self.window.gridlayout_webView.setGeometry(QRect(
                0, 0, values.MAIN_WINDOW_WIDTH - (2 * values.SIDE_TAB_WIDTH),
                values.MAIN_WINDOW_HEIGHT - values.GUI_ITEM_HEIGHT - values.GUI_MENU_HEIGHT))

            # accounts -------------------------------------------------------------------------
            # row 1
            self.window.label_nodeProvider.setObjectName("label_nodeProvider")
            self.window.label_nodeProvider.setText("Node provider:")
            self.window.lineEdit_nodeProvider.setText(values.ETHEREUM_PROVIDER)
            self.window.lineEdit_nodeProvider.setObjectName("lineEdit_nodeProvider")
            self.window.pushButton_nodeProvider.setObjectName("pushButton_nodeProvider")
            self.window.pushButton_nodeProvider.setText("Providers")

            # row 2
            self.window.label_accountName.setObjectName("label_accountName")
            self.window.label_accountName.setText("Account name:")
            self.window.lineEdit_accountName.setObjectName("lineEdit_accountName")
            self.window.pushButton_accountName.setObjectName("pushButton_accountName")
            self.window.pushButton_accountName.setText("Edit")
            self.window.pushButton_deleteAccount.setObjectName("pushButton_deleteAccount")
            self.window.pushButton_deleteAccount.setText('Delete account')

            # row 3
            self.window.label_activeAddress.setObjectName("label_activeAddress")
            self.window.label_activeAddress.setText("Active address:")
            self.window.comboBox_activeAddressVal.setObjectName("comboBox_activeAddressVal")
            self.window.pushButton_copyAddress.setObjectName("pushButton_copyAddress")
            self.window.pushButton_copyAddress.setText("Copy address")

            # row 4
            self.window.label_amount.setObjectName("label_amount")
            self.window.label_amount.setText("Amount:")
            self.window.label_amountVal.setObjectName("label_amountVal")
            self.window.label_amountVal.setText("0")
            self.window.pushButton_etherScan.setObjectName("pushButton_etherScan")
            self.window.pushButton_etherScan.setText("Explorer")

            # row 5
            self.window.label_sendAddress.setObjectName("label_send")
            self.window.label_sendAddress.setText("Send ETH to:")
            self.window.lineEdit_sendAddress.setObjectName("lineEdit_send")
            self.window.pushButton_send.setObjectName("pushButton_send")
            self.window.pushButton_send.setText("Send TX")
            self.window.comboBox_tokens.setObjectName("comboBox_tokens")
            self.window.comboBox_tokens.addItem('Loading tokens...')

            # row 6
            self.window.label_sendValue.setObjectName("label_sendValue")
            self.window.label_sendValue.setText("Value to send:")
            self.window.lineEdit_sendValue.setObjectName("lineEdit_sendValue")
            self.window.label_message.setObjectName("label_message")
            self.window.label_message.setText("Message:")
            self.window.lineEdit_message.setObjectName("lineEdit_message")

            # row 7
            self.window.textEdit_main.setObjectName("textEdit_main")

            # customization
            self.window.label_customizationArea.setObjectName("label_customizationArea")
            self.window.label_customizationArea.setText("Customization area")
            self.window.radioButton_mainNet.setObjectName("radioButton_mainNet")
            self.window.radioButton_mainNet.setText("MainNet")
            self.window.radioButton_testNet.setObjectName("radioButton_testNet")
            self.window.radioButton_testNet.setText("TestNet(Sepolia)")
            self.window.label_GasFeePriority.setObjectName("label_GasFeePriority")
            self.window.label_GasFeePriority.setText("Transaction priority")
            self.window.comboBox_GasFeePriority.setObjectName("comboBox_GasFeePriority")
            self.window.comboBox_GasFeePriority.addItem('high')
            self.window.comboBox_GasFeePriority.addItem('medium')
            self.window.comboBox_GasFeePriority.addItem('low')

            self.window.line_vertical.setObjectName("line_vertical")
            self.window.line_vertical.setFrameShape(QFrame.Shape.VLine)

            # ----------------------------------------------------------------------------------
            self.window.setStatusBar(self.window.statusbar)
            self.window.statusbar.setObjectName("statusbar")
            # ----------------------------------------------------------------------------------
            # row 1
            self.window.gridlayout_accounts.addWidget(self.window.label_nodeProvider, 1, 0, 1, 1)
            self.window.gridlayout_accounts.addWidget(self.window.lineEdit_nodeProvider, 1, 1, 1, 3)
            self.window.gridlayout_accounts.addWidget(self.window.pushButton_nodeProvider, 1, 4, 1, 1)
            self.window.gridlayout_accounts.addWidget(self.window.line_vertical, 1, 5, 6, 1)
            self.window.gridlayout_accounts.addWidget(self.window.label_customizationArea, 1, 6, 1, 1)

            # row 2
            self.window.gridlayout_accounts.addWidget(self.window.label_accountName, 2, 0, 1, 1)
            self.window.gridlayout_accounts.addWidget(self.window.lineEdit_accountName, 2, 1, 1, 2)
            self.window.gridlayout_accounts.addWidget(self.window.pushButton_accountName, 2, 3, 1, 1)
            self.window.gridlayout_accounts.addWidget(self.window.pushButton_deleteAccount, 2, 4, 1, 1)
            # col 5 empty
            self.window.gridlayout_accounts.addWidget(self.window.radioButton_mainNet, 2, 6, 1, 1)

            # row 3
            self.window.gridlayout_accounts.addWidget(self.window.label_activeAddress, 3, 0, 1, 1)
            self.window.gridlayout_accounts.addWidget(self.window.comboBox_activeAddressVal, 3, 1, 1, 3)
            self.window.gridlayout_accounts.addWidget(self.window.pushButton_copyAddress, 3, 4, 1, 1)
            # col 5 empty
            self.window.gridlayout_accounts.addWidget(self.window.radioButton_testNet, 3, 6, 1, 1)

            # row 4
            self.window.gridlayout_accounts.addWidget(self.window.label_amount, 4, 0, 1, 1)
            self.window.gridlayout_accounts.addWidget(self.window.label_amountVal, 4, 1, 1, 2)
            self.window.gridlayout_accounts.addWidget(self.window.comboBox_tokens, 4, 3, 1, 1)
            self.window.gridlayout_accounts.addWidget(self.window.pushButton_etherScan, 4, 4, 1, 1)
            # col 5 empty
            self.window.gridlayout_accounts.addWidget(self.window.label_GasFeePriority, 4, 6, 1, 1)

            # row 5
            self.window.gridlayout_accounts.addWidget(self.window.label_sendAddress, 5, 0, 1, 1)
            self.window.gridlayout_accounts.addWidget(self.window.lineEdit_sendAddress, 5, 1, 1, 3)
            self.window.gridlayout_accounts.addWidget(self.window.pushButton_send, 5, 4, 1, 1)
            # col 5 empty
            self.window.gridlayout_accounts.addWidget(self.window.comboBox_GasFeePriority, 5, 6, 1, 1)

            # row 6
            self.window.gridlayout_accounts.addWidget(self.window.label_sendValue, 6, 0, 1, 1)
            self.window.gridlayout_accounts.addWidget(self.window.lineEdit_sendValue, 6, 1, 1, 1)
            self.window.gridlayout_accounts.addWidget(self.window.label_message, 6, 2, 1, 1)
            self.window.gridlayout_accounts.addWidget(self.window.lineEdit_message, 6, 3, 1, 2)
            # col 5 empty
            # col 6 empty

            # row 7
            self.window.gridlayout_accounts.addWidget(self.window.textEdit_main, 7, 0, 1, 7)

            self.window.comboBox_activeAddressVal.clear()
            self.window.comboBox_tokens.setCurrentIndex(0)
            self.window.comboBox_GasFeePriority.setCurrentIndex(1)
            self.window.radioButton_mainNet.setChecked(True)
            self.window.radioButton_testNet.setChecked(False)
            self.window.lineEdit_accountName.setEnabled(False)
            # webView  -------------------------------------------------------------------------
            self.window.webEngineView.setObjectName("webEngineView")
            self.window.webEngineView.setUrl(QUrl(values.ETHERSCAN_URI))
            self.window.gridlayout_webView.addWidget(self.window.webEngineView, 0, 0, 1, 1)
        except Exception as er:
            print(str(er))
            raise Exception(f"gui_initMainWindow -> initUI -> {er}")

    def initIcons(self):
        try:
            # self.window.setWindowIcon(QtGui.QIcon('icon.png'))
            # self.window.setIconSize(QSize(ICON_SIZE, ICON_SIZE))

            self.window.pushButton_copyAddress.setIcon(QIcon(system.getIconPath('copy.png')))
            self.window.pushButton_copyAddress.setIconSize(QSize(values.ICON_SIZE, values.ICON_SIZE))

            self.window.pushButton_etherScan.setIcon(QIcon(system.getIconPath('ethereum.png')))
            self.window.pushButton_etherScan.setIconSize(QSize(values.ICON_SIZE, values.ICON_SIZE))

            self.window.pushButton_nodeProvider.setIcon(QIcon(system.getIconPath('node.png')))
            self.window.pushButton_nodeProvider.setIconSize(QSize(values.ICON_SIZE, values.ICON_SIZE))

            self.window.pushButton_send.setIcon(QIcon(system.getIconPath('moneyTransfer.png')))
            self.window.pushButton_send.setIconSize(QSize(values.ICON_SIZE, values.ICON_SIZE))

            self.window.pushButton_accountName.setIcon(QIcon(system.getIconPath('edit.png')))
            self.window.pushButton_accountName.setIconSize(QSize(values.ICON_SIZE, values.ICON_SIZE))

            self.window.pushButton_deleteAccount.setIcon(QIcon(system.getIconPath('delete.png')))
            self.window.pushButton_deleteAccount.setIconSize(QSize(values.ICON_SIZE, values.ICON_SIZE))
        except Exception as er:
            raise Exception(f"gui_initMainWindow -> initIcons -> {er}")

    def initStyleSheet(self):
        try:
            mainStyle = (
                "background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,"
                "stop:0 rgb(30, 76, 108) , stop:1 rgb(47, 54, 60));"
                "margin: 0px  0px 0px 0px;"
                "padding: 0px 0px 0px 0px;"  # top, bottom, x ,x;"
            )
            self.window.setStyleSheet(mainStyle)
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
            self.window.menubar_file.setStyleSheet(menuBarStyle)
            menuStyle = (
                "QMenu {background-color: rgb(47, 54, 60); margin: 2px;}"
                "QMenu::item { padding: 2px 25px 2px 20px;  "
                "border-top-left-radius: 10px;}"
                "QMenu::item:selected {border: 2px solid rgb(108, 204, 244); background: rgb(30, 76, 108);}"
                "QMenu::item:pressed {background: rgb(108, 204, 244); color: black}"
            )
            self.window.menu_wallet.setStyleSheet(menuStyle)
            self.window.menu_network.setStyleSheet(menuStyle)

            tabWidgetStyle = (
                "QTabWidget::pane { border: transparent;}"
                "QTabWidget::tab-bar {top: 217px;}"
                "QTabBar::tab:!selected {"
                "background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,"
                "stop:0 rgb(30, 76, 108) , stop:1 rgb(47, 54, 60));"
                "border: 1px solid  rgb(108, 204, 244);"
                "border-top-left-radius: 10px;"
                "border-bottom-right-radius: 10px;"
                f"height: 62px; width: {values.SIDE_TAB_WIDTH}px;"
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
                f"height: 62px; width: {values.SIDE_TAB_WIDTH}px;"
                "padding: 0px 0px 0px 0px;"  # top, right, bottom, left
                "margin: 0px 0px 3px 3px;}"  # top, right, bottom, left
                "color: black"
            )

            self.window.tabWidget_main.setStyleSheet(tabWidgetStyle)

            buttonStyle = (
                "QPushButton {border: 2px solid rgb(108, 204, 244);"
                "border-radius: 12px;"
                "padding: 0px 3px 0px 3px;"  # top, right, bottom, left
                "margin: 0px 0px 0px 0px;"  # top, right, bottom, left
                "text-align: center;"
                "width: 8em;"
                # "border-top-left-radius: 10px;"
                # "border-bottom-right-radius: 10px;"
                f"height: {values.GUI_ITEM_HEIGHT}px;"
                "background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,"
                "stop:0 rgb(30, 76, 108) , stop:1 rgb(47, 54, 60));"
                "min-width: 80px;}"
                "QPushButton:hover {color: black; background-color: rgb(190, 200, 207);}"
                "QPushButton:pressed {background-color: rgb(108, 204, 244);}"
            )
            self.window.pushButton_send.setStyleSheet(buttonStyle)
            self.window.pushButton_etherScan.setStyleSheet(buttonStyle)
            self.window.pushButton_accountName.setStyleSheet(buttonStyle)
            self.window.pushButton_nodeProvider.setStyleSheet(buttonStyle)
            self.window.pushButton_copyAddress.setStyleSheet(buttonStyle)
            self.window.pushButton_deleteAccount.setStyleSheet(buttonStyle)
            labelStyle = (
                "color: white;"
                f"height: {values.GUI_ITEM_HEIGHT}px;"
                "background-color: transparent;"
            )
            self.window.label_sendAddress.setStyleSheet(labelStyle)
            self.window.label_message.setStyleSheet(labelStyle)
            self.window.label_amount.setStyleSheet(labelStyle)
            self.window.label_accountName.setStyleSheet(labelStyle)
            self.window.label_sendValue.setStyleSheet(labelStyle)
            self.window.label_activeAddress.setStyleSheet(labelStyle)
            self.window.label_customizationArea.setStyleSheet(labelStyle)
            self.window.label_nodeProvider.setStyleSheet(labelStyle)
            self.window.label_amountVal.setStyleSheet(labelStyle)
            self.window.label_GasFeePriority.setStyleSheet(labelStyle)

            lineEditStyle = (
                f"height: {values.GUI_ITEM_HEIGHT}px;"
                "background-color: rgb(250, 240, 200); color: black"
            )
            self.window.lineEdit_nodeProvider.setStyleSheet(lineEditStyle)
            self.window.lineEdit_sendAddress.setStyleSheet(lineEditStyle)
            self.window.lineEdit_sendValue.setStyleSheet(lineEditStyle)
            self.window.lineEdit_message.setStyleSheet(lineEditStyle)
            self.window.lineEdit_accountName.setStyleSheet("background-color: transparent; border: none;"
                                                           "color: rgb(108, 204, 244); font-weight: bold;")
            radioButtonStyle = (
                "QRadioButton {background-color: transparent;}"
                "QRadioButton::indicator { width: 24px; height: 12px; border-radius: 7px;}"
                "QRadioButton::indicator:unchecked{border: 1px solid red;}"
                "QRadioButton::indicator:checked{border: 1px solid green;background-image : url("
                f"{system.getIconPath('fill.png')})}}"
                "QRadioButton::indicator:checked:pressed{border: 1px solid white;}"
            )
            self.window.radioButton_testNet.setStyleSheet(radioButtonStyle)
            self.window.radioButton_mainNet.setStyleSheet(radioButtonStyle)
            comboBoxStyle = (
                "background-color: rgb(30, 76, 108); color: black; "
                "selection-background-color: rgb(47, 54, 60); selection-color: white; "
                "padding: 3px 3px 3px 3px;"  # top, right, bottom, left
                "margin: 0px 0px 0px 0px;"  # top, right, bottom, left
                # "text-align: center;"
                "QComboBox::editable {"
                "background-color: transparent;"
                "border: none;"
                "color: rgb(108, 204, 244);"
                "font-weight: bold;"
                "}"
                # "QComboBox:!editable{  background: blue;  font: 11pt 'Walkway Bold'; color: yellow;}"
            )
            self.window.comboBox_activeAddressVal.setStyleSheet(comboBoxStyle)
            self.window.comboBox_GasFeePriority.setStyleSheet(comboBoxStyle)
            self.window.comboBox_tokens.setStyleSheet(comboBoxStyle)

            self.window.textEdit_main.setStyleSheet("background-color: black; color: cyan")

            self.window.resetStatueBarStyleSheet()
        except Exception as er:
            raise Exception(f"gui_initMainWindow -> initStyleSheet -> {er}")

    def setMenuActionsTips(self):
        try:
            # Wallets-New wallet-------------------------------------------------------------------------------------
            self.window.action_newRandomAccount.setShortcut('Ctrl+n')
            self.window.action_newRandomAccount.setStatusTip('create new random account')
            self.window.action_recoverFromMnemonic.setShortcut('Ctrl+m')
            self.window.action_recoverFromMnemonic.setStatusTip('recover an old account from mnemonic')
            self.window.action_recoverFromEntropy.setShortcut('Ctrl+e')
            self.window.action_recoverFromEntropy.setStatusTip('recover an old account from entropy')
            self.window.action_recoverFromPrivateKey.setShortcut('Ctrl+p')
            self.window.action_recoverFromPrivateKey.setStatusTip('recover an old account from the private Key')
            self.window.action_ViewOnlyAccount.setShortcut('Ctrl+w')
            self.window.action_ViewOnlyAccount.setStatusTip('create view only account')
            # Wallets-Secrets---------------------------------------------------------------------------------
            self.window.action_entropy.setShortcut('Alt+e')
            self.window.action_entropy.setStatusTip('see your account entropy')
            self.window.action_privateKey.setShortcut('Alt+p')
            self.window.action_privateKey.setStatusTip('see your account private key')
            # self.window.action_publicKeyCoordinates.setShortcut('Alt+p+c')
            self.window.action_publicKeyCoordinates.setStatusTip('see your account public Key Coordinates')
            self.window.action_publicKey.setShortcut('Alt+k')
            self.window.action_publicKey.setStatusTip('see your account public Key')
            self.window.action_mnemonic.setShortcut('Alt+m')
            self.window.action_mnemonic.setStatusTip('see your account mnemonic words')
            # Wallets-Backup&Restore------------------------------------------------------------------------------
            self.window.action_backup.setShortcut('Ctrl+b')
            self.window.action_backup.setStatusTip('back up your account to file')
            self.window.action_restore.setShortcut('Ctrl+r')
            self.window.action_restore.setStatusTip('restore your account from file')
            # Network-Transactions---------------------------------------------------------------------------------
            self.window.action_checkTx.setShortcut('Alt+t')
            self.window.action_checkTx.setStatusTip('view a transaction details')
            self.window.action_txNonce.setShortcut('Alt+n')
            self.window.action_txNonce.setStatusTip('view sent transaction count')
            self.window.action_simpleHistory.setShortcut('Alt+h')
            self.window.action_simpleHistory.setStatusTip(
                'simple history of your account transactions. up to last 10000 block')
            # self.window.action_allNormal.setShortcut('Alt+n+t')
            self.window.action_allNormal.setStatusTip(
                'simple history of your normal transactions. up to last 10000 block')
            # self.window.action_allInternal.setShortcut('Alt+i+t')
            self.window.action_allInternal.setStatusTip(
                'simple history of your internal transactions. up to last 10000 block')
            # Network-Tools-----------------------------------------------------------------------------------------
            # self.window.action_publicKeyFromTxHash.setShortcut('Alt+m')
            self.window.action_publicKeyFromTxHash.setStatusTip('recover sender public key from transaction hash')
            # self.window.action_transactionMessage.setShortcut('Alt+m')
            self.window.action_transactionMessage.setStatusTip('view the embedded message in a transaction')
            # self.window.action_pendingTransactions.setShortcut('Alt+p')
            self.window.action_pendingTransactions.setStatusTip('view non-verified transactions')
        except Exception as er:
            raise Exception(f"gui_initMainWindow -> setMenuActionsTips -> {er}")
