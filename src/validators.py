from urllib.parse import urlparse
from src.dataTypes import TYPE


def checkHex(value):
    try:
        checkType(value, TYPE.STRING)
        if value.startswith('0x') or value.startswith('0X'):
            value = value[2:]
        int(value, 16)
    except Exception as er:
        raise Exception(f"checkHex -> {er}")


def checkType(value, type_: TYPE):
    try:
        if not isinstance(value, type_.value):
            raise Exception(f"'{value}' is not {type_.value}")
    except Exception as er:
        raise Exception(f"checkType -> {er}")


def checkLen(value, len_: int):
    try:
        if not len(value) == len_:
            raise Exception(f"'{value}' by len {len(value)} received.\nExpected {len_}.")
    except Exception as er:
        raise Exception(f"checkLen -> {er}")


def checkURL(value: str):
    try:
        checkType(value, TYPE.STRING)
        result = urlparse(value)
        return all([result.scheme, result.netloc])
    except Exception as er:
        raise Exception(f"checkURL -> {er}")
