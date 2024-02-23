import webbrowser
import pyperclip
from PyQt6 import QtWidgets, uic
from PyQt6.QtCore import QSize
from PyQt6.QtGui import QIcon, QPixmap


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        # super(Ui, self).__init__()
        uic.loadUi('UI/MainWindow.ui', self)

        self.initIcons()
        self.setClickEvents()
        self.entropy = None
        (self.findChild(QtWidgets.QComboBox, 'comboBox_activeAddress_val')
         .clear())

    def setClickEvents(self):
        (self.findChild(QtWidgets.QPushButton, 'pushButton_copy_address')
         .clicked.connect(self.copyAddress))
        (self.findChild(QtWidgets.QPushButton, 'pushButton_ETH')
         .clicked.connect(self.goToEtherscan))
        (self.findChild(QtWidgets.QPushButton, 'pushButton_node_provider')
         .clicked.connect(self.goToEtherNodes))

    def initIcons(self):
        self.setIcons(QtWidgets.QPushButton, 'pushButton_copy_address',
                      'UI/icons/copy_w.png')
        self.setIcons(QtWidgets.QPushButton, 'pushButton_ETH',
                      'UI/icons/ethereum_c_b.png')
        self.setIcons(QtWidgets.QPushButton, 'pushButton_node_provider',
                      'UI/icons/ethereum_node_clr.png')

    def setIcons(self, elementType, elementName, iconPath, width=16, height=16):
        icon = QIcon()
        icon.addPixmap(QPixmap(iconPath))
        element = self.findChild(elementType, elementName)
        element.setIcon(icon)
        element.setIconSize(QSize(width, height))

    def goToEtherscan(self):
        active_address = self.getComboboxCurrentText('comboBox_activeAddress_val')
        if active_address is not None:
            webbrowser.open('https://etherscan.io/address/' + active_address)

    @staticmethod
    def goToEtherNodes():
        webbrowser.open('https://ethereumnodes.com/')

    def copyAddress(self):
        active_address = self.getComboboxCurrentText('comboBox_activeAddress_val')
        if active_address is not None:
            pyperclip.copy(active_address)
        # spam = pyperclip.paste()

    def changeVisibility(self, elementType, elementName, visibility):
        pass
        # element = self.findChild(elementType, elementName)
        # element.setVisible(visibility)

    def setText(self, elementType, elementName, text):
        self.findChild(elementType, elementName).setText(text)

    def getText(self, elementType, elementName):
        return self.findChild(elementType, elementName).text()

    def addTextToCombobox(self, elementName, text):
        self.findChild(QtWidgets.QComboBox, elementName).addItem(text)

    def getComboboxCurrentText(self, elementName):
        return self.findChild(QtWidgets.QComboBox, elementName).currentText()
