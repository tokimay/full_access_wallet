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
        # return join(basePath, 'resources/icons/', iconName)  # for source run
        return join(basePath, iconName)  # for release
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
