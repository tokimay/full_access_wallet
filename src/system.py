from os.path import join
from pathlib import Path


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
