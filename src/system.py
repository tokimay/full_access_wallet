import os
from pathlib import Path

from src import gui_errorDialog


def getAbsolutePath(relativePath):
    try:
        basePath = Path(__file__).parent.parent
        return os.path.join(basePath, relativePath)
    except Exception as er:
        gui_errorDialog.Error('resourcePath', str(er)).exec()
        return os.path.abspath(".")


def getIconPath(iconName):
    try:
        basePath = Path(__file__).parent.parent
        # return os.path.join(basePath, 'resources/UI/icons/', iconName)
        return os.path.join(basePath, iconName)
    except Exception as er:
        gui_errorDialog.Error('resourcePath', str(er)).exec()
        return os.path.abspath(".")
