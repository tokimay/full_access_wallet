import sys
from src import account, database, gui_mainWindow, qui_create_newAccount, gui_errorDialog
from PyQt6.QtWidgets import QApplication, QMainWindow


app = QApplication(sys.argv)
window = gui_mainWindow.Ui()
window.show()
db = database.sqlite('Data')

if not db.isTableExist():
    createAccount_window = qui_create_newAccount.Ui()
    createAccount_window.exec()
    entropy = createAccount_window.getEntropy()
    if isinstance(entropy, str) and len(entropy) == 256 and entropy != 'init':
        acc = account.fromEntropy(entropy)
        db.createTable()
        print('privateKeyHex', hex(acc['privateKey']), type(acc['privateKey']))
        print('publicKeyCoordinate', acc['publicKeyCoordinate'], type(acc['publicKeyCoordinate']))
        print('publicKey', hex(acc['publicKey']), type(acc['publicKey']))
        print('address', hex(acc['address']), type(acc['address']))
        window.addTextToCombobox('comboBox_activeAddress_val', hex(acc['address']))
        db.insertRow([
            bin(acc['privateKey'])[2:].zfill(256),  # convert hex to 256 bit string binary as entropy
            hex(acc['privateKey']),
            hex(acc['publicKeyCoordinate'][0]),
            hex(acc['publicKeyCoordinate'][1]),
            hex(acc['publicKey']),
            hex(acc['address'])
        ])
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
    window.addTextToCombobox('comboBox_activeAddress_val', accounts[0])

app.exec()
