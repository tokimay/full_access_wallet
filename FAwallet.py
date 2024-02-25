import sys
from src import account, database, gui_mainWindow, qui_create_newAccount, gui_errorDialog, types
from PyQt6.QtWidgets import QApplication, QMainWindow

from src.threads import Balance

dbName = 'Data'
app = QApplication(sys.argv)
window = gui_mainWindow.Ui(dbName)
window.show()
db = database.Sqlite(dbName)
db.createTable()

getBalance = False

if not db.isAccountExist():
    address = account.createAccount(db, "There is no account")
    if address != 'None':
        window.comboBox_activeAddress_val.addItem(address)
        getBalance = True
else:
    accounts = (db.readColumn(types.SECRET.ADDRESS))
    for ad in accounts:
        window.comboBox_activeAddress_val.addItem(ad[0])
    getBalance = True

if getBalance:
    balanceThread = Balance(window)
    balanceThread.finished.connect(app.exit)
    balanceThread.start()

app.exec()
