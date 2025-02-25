
# This file is part of https://github.com/tokimay/full_access_wallet
# Copyright (C) 2016 https://github.com/tokimay
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
# This software is licensed under GPLv3. If you use or modify this project,
# you must include a reference to the original repository: https://github.com/tokimay/full_access_wallet

from PyQt6 import QtWidgets, QtCore
from PyQt6.QtWidgets import QDialog


class WINDOW(QDialog):
    def __init__(self, title: str, messageHeader: str, messageBody: str):
        super().__init__()
        self.userAnswer = False
        self.title = title
        self.messageHeader = messageHeader
        self.messageBody = messageBody

        self.gridLayout = QtWidgets.QGridLayout(self)
        self.label_messageHeader = QtWidgets.QLabel()
        self.label_messageBody = QtWidgets.QLabel()
        self.pushButton_yes = QtWidgets.QPushButton()
        self.pushButton_no = QtWidgets.QPushButton()
        self.initUI()
        self.setClickEvents()

    def initUI(self):
        self.setObjectName("user choice")
        self.resize(320, 150)
        self.gridLayout.addWidget(self.label_messageHeader)
        self.gridLayout.addWidget(self.label_messageBody)
        self.gridLayout.addWidget(self.pushButton_yes)
        self.gridLayout.addWidget(self.pushButton_no)

        self.gridLayout.setGeometry(QtCore.QRect(0, 0, 320, 150))
        self.gridLayout.setObjectName("gridLayoutWidget")
        self.gridLayout.setContentsMargins(10, 10, 10, 10)

        self.gridLayout.setColumnStretch(4, 3)
        self.gridLayout.addWidget(self.label_messageHeader, 0, 0, 1, 4)
        self.gridLayout.addWidget(self.label_messageBody, 1, 0, 1, 4)
        self.gridLayout.addWidget(self.pushButton_no, 2, 1, 1, 1)
        self.gridLayout.addWidget(self.pushButton_yes, 2, 2, 1, 1)

        self.setWindowTitle(self.title)

        self.label_messageHeader.setEnabled(True)
        self.label_messageHeader.setObjectName("label_messageHeader")
        self.label_messageHeader.setText(self.messageHeader)

        self.label_messageBody.setEnabled(True)
        self.label_messageBody.setObjectName("label_messageBody")
        self.label_messageBody.setText(self.messageBody)

        self.pushButton_no.setObjectName("pushButton_no")
        self.pushButton_no.setText("No")

        self.pushButton_yes.setObjectName("pushButton_yes")
        self.pushButton_yes.setText("Yes")

    def setClickEvents(self):
        self.pushButton_yes.clicked.connect(self.yes)
        self.pushButton_no.clicked.connect(self.no)

    def yes(self):
        self.userAnswer = True
        self.close()

    def no(self):
        self.userAnswer = False
        self.close()

    def getAnswer(self):
        return self.userAnswer
