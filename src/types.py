from enum import Enum


class SECRET(Enum):
    ENTROPY = 'ENT'
    PRIVATE_KEY = 'PRV'
    PUBLIC_KEY_X = 'PUK_COR_X'
    PUBLIC_KEY_Y = 'PUK_COR_Y'
    PUBLIC_KEY = 'PUK'
    ADDRESS = 'ADR'
    MNEMONIC = 'NEM'


class TYPE(Enum):
    STRING = str
    INTEGER = int
    DICTIONARY = dict
    LIST = list
    TUPLE = tuple
    FLOAT = float
    BOOLEAN = bool

