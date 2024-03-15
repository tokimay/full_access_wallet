from sys import argv
from PyQt6.QtWidgets import QApplication
from src import database, dataTypes
from src.GUI import gui_mainWindow, gui_userChoice, gui_error, gui_message
from src.threads import Balance

dbName = 'Data'
app = QApplication(argv)
window = gui_mainWindow.Ui(dbName)
window.show()
db = database.Sqlite(dbName)
db.createTable()
getBalance = False

if db.isAccountExist():
    accounts = db.readColumnAllRows(dataTypes.SECRET.ADDRESS.value)
    for ad in accounts:
        window.comboBox_activeAddressVal.addItem(ad[0])
        accountName = db.readColumn('NAM', window.comboBox_activeAddressVal.currentText())
        window.lineEdit_accountName.setText(str(accountName[0][0]))
    getBalance = True
else:  # there is no account in database
    createAccount_window = gui_userChoice.WINDOW('Create new account', 'There is no account!',
                                                 'Create new one?')
    createAccount_window.exec()
    if not createAccount_window.getAnswer():  # cancel by user
        gui_message.WINDOW('Create new account', 'You always can create new account or restore old one',
                           'Wallet -> New account').exec()
    else:  # create first new account
        window.createAccountRandom()
if getBalance:
    balanceThread = Balance(window)
    balanceThread.finished.connect(app.exit)
    balanceThread.start()
app.exec()

