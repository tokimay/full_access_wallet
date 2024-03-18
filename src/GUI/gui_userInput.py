from PyQt6 import QtWidgets, QtCore
from PyQt6.QtWidgets import QDialog


class WINDOW(QDialog):
    def __init__(self, title: str, messageHeader: str):
        super().__init__()
        self.userAnswer = False
        self.title = title
        self.messageHeader = messageHeader
        self.input = ''

        self.gridLayout = QtWidgets.QGridLayout(self)
        self.label_messageHeader = QtWidgets.QLabel()
        self.textEdit_input = QtWidgets.QTextEdit()
        self.pushButton_ok = QtWidgets.QPushButton()
        self.pushButton_cancel = QtWidgets.QPushButton()
        self.initUI()
        self.setClickEvents()

    def initUI(self):
        self.setObjectName("user choice")
        self.resize(280, 150)
        self.gridLayout.addWidget(self.label_messageHeader)
        self.gridLayout.addWidget(self.textEdit_input)
        self.gridLayout.addWidget(self.pushButton_ok)
        self.gridLayout.addWidget(self.pushButton_cancel)

        self.gridLayout.setGeometry(QtCore.QRect(0, 0, 280, 150))
        self.gridLayout.setObjectName("gridLayoutWidget")
        self.gridLayout.setContentsMargins(10, 10, 10, 10)

        self.gridLayout.setColumnStretch(6, 3)
        self.gridLayout.addWidget(self.label_messageHeader, 0, 0, 1, 6)
        self.gridLayout.addWidget(self.textEdit_input, 1, 0, 1, 6)
        self.gridLayout.addWidget(self.pushButton_cancel, 2, 2, 1, 1)
        self.gridLayout.addWidget(self.pushButton_ok, 2, 3, 1, 1)

        self.setWindowTitle(self.title)

        self.label_messageHeader.setEnabled(True)
        self.label_messageHeader.setObjectName("label_messageHeader")
        self.label_messageHeader.setText(self.messageHeader)

        self.textEdit_input.setEnabled(True)
        self.textEdit_input.setObjectName("lineEdit_input")

        self.pushButton_cancel.setObjectName("pushButton_no")
        self.pushButton_cancel.setText("No")

        self.pushButton_ok.setObjectName("pushButton_yes")
        self.pushButton_ok.setText("Yes")

    def setClickEvents(self):
        self.pushButton_ok.clicked.connect(self.ok)
        self.pushButton_cancel.clicked.connect(self.cancel)
        self.textEdit_input.installEventFilter(self)

    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.Type.KeyPress and obj is self.textEdit_input:
            if (event.key() == QtCore.Qt.Key.Key_Return or event.key() == QtCore.Qt.Key.Key_Enter
            ) and self.textEdit_input.hasFocus():
                self.ok()
        return super().eventFilter(obj, event)

    def ok(self):
        self.input = self.textEdit_input.toPlainText()
        self.close()

    def cancel(self):
        self.input = ''
        self.close()

    def getInput(self):
        return self.input
