import sys
from src import account, database, gui_mainWindow, types, qui_getUserChoice, qui_showMessage, gui_errorDialog
from PyQt6.QtWidgets import QApplication

from src.threads import Balance

dbName = 'Data'
app = QApplication(sys.argv)
window = gui_mainWindow.Ui(dbName)
window.show()
db = database.Sqlite(dbName)
db.createTable()

getBalance = False

if db.isAccountExist():
    accounts = (db.readColumn(types.SECRET.ADDRESS))
    for ad in accounts:
        window.comboBox_activeAddress_val.addItem(ad[0])
    getBalance = True

else:
    createAccount_window = qui_getUserChoice.Ui('Create new account',
                                                'There is no account!',
                                                'Create new one?')
    createAccount_window.exec()
    if not createAccount_window.getAnswer():
        qui_showMessage.Ui('Create new account',
                           'You always can create new account or restore old one',
                           'Wallet -> New account').exec()
    else:
        acc = account.New.random()
        if len(acc) == 0:
            pass
        else:
            mnemonic = account.New.generateMnemonic(acc['entropy'])
            if mnemonic == '':
                err = gui_errorDialog.Error('Account creation failed in mnemonic step')
                err.exec()
            else:
                acc['mnemonic'] = str(mnemonic)  # append mnemonic to dict
                db.insertRow(acc)
                window.comboBox_activeAddress_val.addItem(acc['address'])
                getBalance = True

if getBalance:
    balanceThread = Balance(window)
    balanceThread.finished.connect(app.exit)
    balanceThread.start()

app.exec()
