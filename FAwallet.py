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
    accounts = db.readColumn(types.SECRET.ADDRESS)
    for ad in accounts:
        window.comboBox_activeAddress_val.addItem(ad[0])
    getBalance = True
else:  # there is no account in database
    createAccount_window = qui_getUserChoice.Ui('Create new account',
                                                'There is no account!',
                                                'Create new one?')
    createAccount_window.exec()
    if not createAccount_window.getAnswer():  # cancel by user
        qui_showMessage.Ui('Create new account',
                           'You always can create new account or restore old one',
                           'Wallet -> New account').exec()
    else:  # create first new account
        acc = account.New.random()
        if len(acc) == 0:  # random account creation return by some error
            pass
        elif not isinstance(acc, dict) or len(acc) == 0:
            gui_errorDialog.Error('Account creation failed \n ' + str(type(acc))).exec()
        else:
            db.insertRow(acc)
            window.comboBox_activeAddress_val.addItem(acc['address'])
            getBalance = True

if getBalance:
    balanceThread = Balance(window)
    balanceThread.finished.connect(app.exit)
    balanceThread.start()

app.exec()
