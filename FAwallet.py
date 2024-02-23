import sys

from src import account, database
from src.gui_mainWindow import Ui as mainUI
from src.qui_create_newAccount import Ui as newAccountUI

from PyQt6.QtWidgets import QApplication
from PyQt6 import QtWidgets

app = QApplication(sys.argv)
window = mainUI()
window.show()

db = database.sqlite('Data')

if not db.isTableExist():
    windowAccount = newAccountUI()
    windowAccount.exec()
    entropy = windowAccount.getRandomEntropy()
    if entropy is not None:
        db.createTable()
        acc = account.new.fromEntropy(entropy)
        print('privateKeyHex', hex(acc['privateKey']), type(acc['privateKey']))
        print('publicKeyCoordinate', acc['publicKeyCoordinate'], type(acc['publicKeyCoordinate']))
        print('publicKey', hex(acc['publicKey']), type(acc['publicKey']))
        print('address', hex(acc['address']), type(acc['address']))
        window.addTextToCombobox('comboBox_activeAddress_val', hex(acc['address']))
        db.insertRow([
            entropy,
            hex(acc['privateKey']),
            hex(acc['publicKeyCoordinate'][0]),
            hex(acc['publicKeyCoordinate'][1]),
            hex(acc['publicKey']),
            hex(acc['address'])
        ])
else:
    accounts = (db.readAllRows())[0]
    window.addTextToCombobox('comboBox_activeAddress_val', accounts[5])

app.exec()
