from PyQt6 import QtWidgets, QtCore
from PyQt6.QtWidgets import QDialog


class Ui(QDialog):
    def __init__(self, title: str, messageHeader: str, messageBody: str):
        super().__init__()
        self.userAnswer = False
        self.title = title
        self.messageHeader = messageHeader
        self.messageBody = messageBody

        self.gridLayout = QtWidgets.QGridLayout(self)
        self.label_messageHeader = QtWidgets.QLabel()
        self.label_messageBody = QtWidgets.QLabel()
        self.pushButton_ok = QtWidgets.QPushButton()

        self.initUI()
        self.setClickEvents()

    def initUI(self):
        self.setObjectName("user choice")
        self.resize(320, 150)

        self.gridLayout.addWidget(self.label_messageHeader)
        self.gridLayout.addWidget(self.label_messageBody)
        self.gridLayout.addWidget(self.pushButton_ok)
        self.gridLayout.setGeometry(QtCore.QRect(0, 0, 320, 150))
        self.gridLayout.setObjectName("gridLayoutWidget")
        self.gridLayout.setContentsMargins(10, 10, 10, 10)

        self.gridLayout.setColumnStretch(3, 3)
        self.gridLayout.addWidget(self.label_messageHeader, 0, 0, 1, 3)
        self.gridLayout.addWidget(self.label_messageBody, 1, 0, 1, 3)
        self.gridLayout.addWidget(self.pushButton_ok, 2, 1, 1, 1)

        self.setWindowTitle(self.title)

        self.label_messageHeader.setEnabled(True)
        self.label_messageHeader.setObjectName("label_messageHeader")
        self.label_messageHeader.setText(self.messageHeader)

        self.label_messageBody.setEnabled(True)
        self.label_messageBody.setObjectName("label_messageBody")
        self.label_messageBody.setText(self.messageBody)

        self.pushButton_ok.setObjectName("pushButton_OK")
        self.pushButton_ok.setText("OK")

    def setClickEvents(self):
        self.pushButton_ok.clicked.connect(self.closeWindow)

    def closeWindow(self):
        self.close()
