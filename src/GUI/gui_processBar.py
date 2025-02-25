
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

from PyQt6.QtWidgets import QProgressBar, QDialog, QVBoxLayout, QListWidget
from src import network, system, threads


class AddTokensToDatabase(QDialog):
    def __init__(self, db):
        try:
            super(AddTokensToDatabase, self).__init__()
            tokens = network.getTokenList()
            self.count = len(tokens['list'])
            self.setWindowTitle('Syncing tokens list..')
            self.progress = QProgressBar(self)
            self.progress.setValue(0)
            self.resize(300, 400)
            self.progress.resize(300, 50)
            self.vbox = QVBoxLayout()
            self.listWidget = QListWidget()
            self.listWidget.resize(300, 350)
            self.vbox.addWidget(self.progress)
            self.vbox.addWidget(self.listWidget)
            self.setLayout(self.vbox)
            self.progress.setMaximum(self.count)
            self.thread = threads.AddToken(db, tokens, self.listWidget)
            self.thread.signalData.connect(self.signalAccept)
            self.thread.error.connect(self.exception)
            self.thread.start()
        except Exception as er:
            system.errorSignal.newError.emit(f"AddTokens -> __init__ -> {str(er)}")

    def signalAccept(self, msg):
        try:
            if msg == self.count:
                self.endProgress()
            else:
                self.progress.setValue(int(msg))
        except Exception as er:
            system.errorSignal.newError.emit(f"AddTokens -> signal_accept -> {str(er)}")

    def endProgress(self):
        try:
            self.close()
        except Exception as er:
            system.errorSignal.newError.emit(f"AddTokens -> endProgress -> {str(er)}")

    def exception(self, message):
        self.thread.terminate()
        system.errorSignal.newError.emit(f"AddTokens -> __init__ -> {message}")

    def closeEvent(self, evnt):
        self.thread.terminate()


