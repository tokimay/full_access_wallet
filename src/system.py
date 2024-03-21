from os.path import join
from pathlib import Path
from PyQt6.QtCore import QObject, pyqtSignal
from src.GUI import gui_error


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
        # for source run
        # return join(basePath, 'resources/icons/', iconName)
        # for release
        return join(basePath, iconName)
    except Exception as er:
        raise Exception('getIconPath ->', str(er))


class Emitter(QObject):
    newError = pyqtSignal(str)


def error(message: str):
    gui_error.WINDOW('FAwallet', f"{message}").exec()


errorSignal = Emitter()
errorSignal.newError.connect(error)


class FAwalletException(Exception):
    def __init__(self, message):
        super().__init__(message)
        raise Exception(message)
