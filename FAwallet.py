import sys
from src import account, database, dataTypes
from src.GUI import gui_mainWindow, qui_getUserChoice, gui_errorDialog, qui_showMessage
from PyQt6.QtWidgets import QApplication
from src.threads import Balance

dbName = 'Data'
app = QApplication(sys.argv)
window = gui_mainWindow.Ui(dbName)
window.show()
db = database.Sqlite(dbName)
if not db.createTable():
    gui_errorDialog.Error('FAWallet createTable', 'Data base error..\n ').exec()

getBalance = False

if db.isAccountExist():
    accounts = db.readColumnAllRows(dataTypes.SECRET.ADDRESS.value)
    for ad in accounts:
        window.comboBox_activeAddressVal.addItem(ad[0])
        accountName = db.readColumnByCondition('NAM', window.comboBox_activeAddressVal.currentText())
        window.lineEdit_accountName.setText(str(accountName[0][0]))
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
            gui_errorDialog.Error('FAWallet createT',
                                  f'Account creation failed \n {str(type(acc))}').exec()
        else:
            if db.insertRow(acc):
                window.comboBox_activeAddressVal.addItem(acc['address'])
                getBalance = True
            else:
                gui_errorDialog.Error('FAWallet createT',
                                      'Inserting account details to database failed.\n').exec()

if getBalance:
    balanceThread = Balance(window)
    balanceThread.finished.connect(app.exit)
    balanceThread.start()

app.exec()
