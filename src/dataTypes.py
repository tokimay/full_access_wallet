from enum import Enum


class TYPE(Enum):
    STRING = str
    INTEGER = int
    DICTIONARY = dict
    LIST = list
    TUPLE = tuple
    FLOAT = float
    BOOLEAN = bool


class ACCOUNT(Enum):
    NAME = 'NAM'
    ADDRESS = 'ADR'
    ENTROPY = 'ENT'
    PRIVATE_KEY = 'PRK'
    PUBLIC_KEY_X = 'PUX'
    PUBLIC_KEY_Y = 'PUY'
    PUBLIC_KEY = 'PUK'
    MNEMONIC = 'NEM'


class TOKEN(Enum):
    NAME = 'NAM'
    ADDRESS = 'ADR'
    SYMBOL = 'SYM'
    TYPE = 'TYP'
    DECIMALS = 'DML'
    LOGO = 'LGU'
    ABI = 'ABI'
