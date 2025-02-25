
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

from PyQt6.QtWidgets import QApplication
from sys import argv
from src import values, database
from src.GUI import gui_error, gui_mainWindow, gui_processBar

APP = QApplication(argv)


db = database.SQLITE(values.DB_NAME)
try:
    db.initializeNew()
    if db.isTableEmpty(values.TABLE_TOKEN):
        gui_processBar.AddTokensToDatabase(db).exec()
except Exception as er:
    gui_error.WINDOW('FAwallet', str(er)).exec()
    exit()
window = gui_mainWindow.Ui(values.DB_NAME)
window.show()
APP.exec()
