import sys
import src.sql as sql

from src.gui_mainWindow import Ui as mainUI
from src.qui_create_newAccount import Ui as newAccountUI

from PyQt6.QtWidgets import QApplication
from PyQt6 import QtWidgets
from eth_account import Account


app = QApplication(sys.argv)
window = mainUI()
window.show()

sql.sqlInit()
if not sql.isTableExist():
    windowAccount = newAccountUI()
    windowAccount.exec()
    entropy = windowAccount.getRandomEntropy()
    if entropy is not None:
        sql.createTable()
        acct = Account.create(int(entropy, 16))
        window.setText('label_activeAddress_val', QtWidgets.QLabel, acct.address)

    """    
    def changeVisibility(self, elementName, elementType, visibility):
        element = self.findChild(elementType, elementName)
        element.setVisible(visibility)


    def generatePrivateKey(self):
        pass
        """
else:
    window.changeVisibility('pushButton_create_account', QtWidgets.QPushButton, False)
    window.changeVisibility('label_no_account', QtWidgets.QLabel, False)

app.exec()
