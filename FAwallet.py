from PyQt6.QtWidgets import QApplication
from sys import argv
from src import values, threads, database, dataTypes, data
from src.GUI import gui_error, gui_mainWindow, gui_userChoice, gui_message

APP = QApplication(argv)


db = database.SQLITE(values.DB_NAME)
getBalance = False

try:
    db.initializeNew()
    if db.isTableEmpty(values.TABLE_TOKEN):
        data.AddTokens(db).exec()
except Exception as er:
    gui_error.WINDOW('FAwallet', str(er)).exec()
    exit()

window = gui_mainWindow.Ui(values.DB_NAME)
window.show()

try:
    if db.isTableEmpty('accounts'):  # there is no account in database
        createAccount_window = gui_userChoice.WINDOW('Create new account', 'There is no account!',
                                                     'Create new one?')
        createAccount_window.exec()
        if not createAccount_window.getAnswer():  # cancel by user
            gui_message.WINDOW('Create new account', 'You always can create new account or restore old one',
                               'Wallet -> New account').exec()
        else:  # create first new account
            window.createAccountRandom()
            getBalance = True
    else:
        accounts = db.readColumnAllRows('accounts', dataTypes.ACCOUNT.ADDRESS.value)
        for ad in accounts:
            window.comboBox_activeAddressVal.addItem(ad[0])
            accountName = db.readColumn('accounts', 'NAM', 'ADR',
                                        window.comboBox_activeAddressVal.currentText())
            window.lineEdit_accountName.setText(str(accountName[0][0]))
        getBalance = True
    if getBalance:
        balanceThread = threads.GetBalance(window)
        balanceThread.finished.connect(APP.exit)
        balanceThread.start()
except Exception as er:
    gui_error.WINDOW('FAwallet', str(er)).exec()
    exit()

APP.exec()
