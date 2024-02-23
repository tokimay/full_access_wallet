from PyQt6 import QtWidgets, uic
from PyQt6.QtCore import QSize
from PyQt6.QtGui import QIcon, QPixmap
import webbrowser


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        # super(Ui, self).__init__()
        uic.loadUi('UI/MainWindow.ui', self)

        self.initIcons()
        self.setClickEvents()
        self.entropy = None

    def setClickEvents(self):
        pushButton_ETH = self.findChild(QtWidgets.QPushButton, 'pushButton_ETH')
        pushButton_ETH.clicked.connect(self.goToEtherscan)

    def initIcons(self):
        self.setIcons('pushButton_copy_address', QtWidgets.QPushButton, 'UI/icons/copy_w.png')
        self.setIcons('pushButton_ETH', QtWidgets.QPushButton, 'UI/icons/ethereum_c_b.png')

    def setIcons(self, elementName, elementType, iconPath, width=16, height=16):
        icon = QIcon()
        icon.addPixmap(QPixmap(iconPath))
        element = self.findChild(elementType, elementName)
        element.setIcon(icon)
        element.setIconSize(QSize(width, height))

    def changeVisibility(self, elementName, elementType, visibility):
        pass
        #element = self.findChild(elementType, elementName)
        #element.setVisible(visibility)

    def setText(self, elementName, elementType, text):
        self.findChild(elementType, elementName).setText(text)

    def getText(self, elementName, elementType):
        return self.findChild(elementType, elementName).text()

    def goToEtherscan(self):
        active_address = self.findChild(QtWidgets.QLabel, 'label_activeAddress_val').text()
        if not active_address == 'None':
            webbrowser.open('https://etherscan.io/address/' + active_address)

    def getRandomEntropy(self):
        pass
        #childWindow = MouseTracker()
        #childWindow.exec()
        #self.entropy = childWindow.getEntropy()

    def generatePrivateKey(self):
        pass

    def createAccount(self):
        pass
        #self.getRandomEntropy()
        #print(self.entropy)
        #print(int(str(self.entropy), 16))
        #self.changeVisibility('pushButton_create_account', QtWidgets.QPushButton, False)
        #self.changeVisibility('label_no_account', QtWidgets.QLabel, False)
        #acct = Account.create(int(self.entropy, 16))
        #print(acct.address)
