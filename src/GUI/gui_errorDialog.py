from PyQt6 import QtWidgets, QtCore
from PyQt6.QtWidgets import QDialog


class Error(QDialog):
    def __init__(self, function: str, message: str):
        super().__init__()
        self.message = message
        self.function = function
        self.gridLayoutWidget = QtWidgets.QWidget(parent=self)
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.plainTextEdit_error = QtWidgets.QPlainTextEdit(parent=self.gridLayoutWidget)
        self.label_1 = QtWidgets.QLabel(parent=self.gridLayoutWidget)
        self.label_2 = QtWidgets.QLabel(parent=self.gridLayoutWidget)
        self.initUI()

    def initUI(self):
        self.setGeometry(500, 250, 315, 240)
        self.setObjectName("Dialog_error")
        self.setWindowTitle(f'Error in {self.function}')
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 10, 300, 220))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.plainTextEdit_error.setObjectName("plainTextEdit_error")
        self.gridLayout.addWidget(self.plainTextEdit_error, 2, 0, 1, 1)
        self.label_1.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.label_1.setObjectName("label_1")
        self.gridLayout.addWidget(self.label_1, 0, 0, 1, 1)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.label_1.setText("Some error has been occurred")
        self.label_2.setText("Error details:")
        self.plainTextEdit_error.setPlainText(self.message)






