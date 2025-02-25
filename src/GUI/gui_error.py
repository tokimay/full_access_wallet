
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
    def __init__(self, title: str, message: str):
        super().__init__()
        self.message = message
        self.function = title
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
