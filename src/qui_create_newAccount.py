import src.account as account
from PyQt6 import QtWidgets, QtCore
from PyQt6.QtWidgets import QDialog


class Ui(QDialog):
    def __init__(self):
        super().__init__()
        self.entropy = 'init'
        self.gridLayoutWidget = QtWidgets.QWidget(parent=self)
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.label_create_account = QtWidgets.QLabel(parent=self.gridLayoutWidget)
        self.pushButton_create_account = QtWidgets.QPushButton(parent=self.gridLayoutWidget)
        self.label_no_account = QtWidgets.QLabel(parent=self.gridLayoutWidget)
        self.pushButton_cancel = QtWidgets.QPushButton(parent=self.gridLayoutWidget)
        self.initUI()
        self.setClickEvents()

    def initUI(self):
        self.setObjectName("create_account_box")
        self.resize(320, 150)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(0, 0, 321, 151))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.label_create_account.setObjectName("label_create_account")
        self.gridLayout.addWidget(self.label_create_account, 2, 1, 1, 2)
        self.pushButton_create_account.setObjectName("pushButton_create_account")
        self.gridLayout.addWidget(self.pushButton_create_account, 4, 1, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding,
                                           QtWidgets.QSizePolicy.Policy.Minimum)
        self.gridLayout.addItem(spacerItem, 4, 0, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding,
                                            QtWidgets.QSizePolicy.Policy.Minimum)
        self.gridLayout.addItem(spacerItem1, 4, 3, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum,
                                            QtWidgets.QSizePolicy.Policy.Expanding)
        self.gridLayout.addItem(spacerItem2, 5, 2, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum,
                                            QtWidgets.QSizePolicy.Policy.Expanding)
        self.gridLayout.addItem(spacerItem3, 0, 1, 1, 1)
        self.label_no_account.setEnabled(True)
        self.label_no_account.setObjectName("label_no_account")
        self.gridLayout.addWidget(self.label_no_account, 1, 1, 1, 2)
        self.pushButton_cancel.setObjectName("pushButton_cancel")
        self.gridLayout.addWidget(self.pushButton_cancel, 4, 2, 1, 1)
        spacerItem4 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum,
                                            QtWidgets.QSizePolicy.Policy.Expanding)
        self.gridLayout.addItem(spacerItem4, 3, 1, 1, 1)
        self.setWindowTitle("Create new account")
        self.label_create_account.setText("Create new account?")
        self.pushButton_create_account.setText("Yes")
        self.label_no_account.setText("There is no account")
        self.pushButton_cancel.setText("No")

    def setClickEvents(self):
        self.pushButton_create_account.clicked.connect(self.createAccount)
        self.pushButton_cancel.clicked.connect(self.cancel)

    def createAccount(self):
        self.close()
        self.entropy = account.generateEntropy()

    def cancel(self):
        self.close()

    def getEntropy(self):
        return self.entropy




