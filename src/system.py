
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

from os.path import join
from pathlib import Path
from PyQt6.QtCore import QObject, pyqtSignal
from src.GUI import gui_error
from time import gmtime, strftime


def getRoot():
    try:
        return Path(__file__).parent.parent
    except Exception as er:
        raise Exception('getRoot ->', str(er))


def getAbsolutePath(relativePath: str) -> str:
    try:
        basePath = Path(__file__).parent.parent
        return join(basePath, relativePath)
    except Exception as er:
        raise Exception('getAbsolutePath ->', str(er))


def getIconPath(iconName: str) -> str:
    try:
        basePath = Path(__file__).parent.parent
        return join(basePath, 'resources/icons/', iconName)  # for source run
        # return join(basePath, iconName)  # for release
    except Exception as er:
        raise Exception('getIconPath ->', str(er))


class Emitter(QObject):
    newError = pyqtSignal(str)


def error(message: str):
    gui_error.WINDOW('FAwallet', f"{strftime('%H:%M:%S', gmtime())}: {message}").exec()


errorSignal = Emitter()
errorSignal.newError.connect(error)


class FAwalletException(Exception):
    def __init__(self, message):
        super().__init__(message)
        raise Exception(message)
