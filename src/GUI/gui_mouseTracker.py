
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

from PyQt6.QtWidgets import QDialog


class WINDOW(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.setMouseTracking(True)
        self.entropy = ''
        self.addNew = True
        self.eventSelector = True
        self.size = 256
        self.setWindowTitle('Move mouse in box randomly')

    def initUI(self):
        self.setGeometry(100, 100, 500, 500)
        self.setWindowTitle('Mouse Tracker')

    def mouseMoveEvent(self, event):
        div = 8192
        if len(self.entropy) > (div + self.size):
            self.entropy = self.entropy[int(div/2):int((div/2) + self.size)]
            self.addNew = False
            self.setWindowTitle('100% Done close the window now')
            self.close()
        else:
            if self.addNew:
                self.setWindowTitle(
                        '({} : {}) {}%'.format(
                            event.scenePosition().x(),
                            event.scenePosition().y(),
                            int(len(self.entropy * 100) / (div + self.size))
                        ))
                if self.eventSelector:
                    self.entropy = self.entropy + bin(int(event.scenePosition().x()))[2:]
                    self.eventSelector = False
                else:
                    self.entropy = self.entropy + bin(int(event.scenePosition().y()))[2:]
                    self.eventSelector = True

    def getEntropy(self):
        return self.entropy
