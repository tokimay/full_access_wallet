from urllib.parse import urlparse

from src.GUI import gui_errorDialog
from src.dataTypes import TYPE


def checkHex(caller: str, value) -> bool:
    try:
        if not ('checkHex', value, TYPE.STRING):
            gui_errorDialog.Error(f'Error in {caller}',
                                  f'({value})\n by type {type(value)} received.\n'
                                  f'Expected string.').exec()
            return False
        else:
            int(value, 16)
            return True
    except ValueError:
        gui_errorDialog.Error(f'Error in {caller}',
                              f'{value} \n'
                              f'is not in hex format').exec()
        return False


def checkType(caller: str, value, type_: TYPE) -> bool:
    if isinstance(value, type_.value):
        return True
    else:
        gui_errorDialog.Error(f'Error in {caller}',
                              f'({value})\n by type {type(value)} received.\n'
                              f'Expected {type_.value}.').exec()
        return False


def checkLen(caller: str, value, len_: int) -> bool:
    if len(value) == len_:
        return True
    else:
        gui_errorDialog.Error(f'Error in {caller}',
                              f'({value})\n by len {len(value)} received.\n'
                              f'Expected {len_}.').exec()
        return False


def checkURL(caller: str, value: str):
    try:
        if not ('checkURL', value, TYPE.STRING):
            gui_errorDialog.Error(f'Error in {caller}',
                                  f'({value})\n by type {type(value)} received.\n'
                                  f'Expected string.').exec()
            return False
        else:

            result = urlparse(value)
            return all([result.scheme, result.netloc])
    except ValueError:
        return False
