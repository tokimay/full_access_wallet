import sys
from src import account, database, gui_mainWindow, qui_create_newAccount, gui_errorDialog
from PyQt6.QtWidgets import QApplication, QMainWindow

from src.threads import Balance

app = QApplication(sys.argv)
window = gui_mainWindow.Ui()
window.show()
db = database.Sqlite('Data')
getBalance = False

if not db.isTableExist():
    createAccount_window = qui_create_newAccount.Ui()
    createAccount_window.exec()
    entropy = createAccount_window.getEntropy()
    if isinstance(entropy, str) and len(entropy) == 256 and entropy != 'init':
        acc = account.fromEntropy(entropy)
        if isinstance(acc, dict):
            db.createTable()
            # print('privateKeyHex', hex(acc['privateKey']), type(acc['privateKey']))
            # print('publicKeyCoordinate', acc['publicKeyCoordinate'], type(acc['publicKeyCoordinate']))
            # print('publicKey', hex(acc['publicKey']), type(acc['publicKey']))
            # print('address', hex(acc['address']), type(acc['address']))
            window.comboBox_activeAddress_val.addItem(hex(acc['address']))
            db.insertRow(acc)
            getBalance = True
        else:
            err = gui_errorDialog.Error('Account creation failed \n ' + str(type(acc)))
            err.show()
    else:
        if entropy == 'init':
            pass
        elif not isinstance(entropy, str):
            err = gui_errorDialog.Error('Entropy received by type ' + str(type(entropy)) + '.\nexpected string')
            err.show()
        else:
            err = gui_errorDialog.Error('Entropy by len ' + str(len(entropy)) + ' bit received.\nexpected 256 bit')
            err.show()
else:
    accounts = (db.readColumn('ADR'))[0]
    window.comboBox_activeAddress_val.addItem(accounts[0])
    getBalance = True

if getBalance:
    balanceThread = Balance(window)
    balanceThread.finished.connect(app.exit)
    balanceThread.start()

app.exec()
