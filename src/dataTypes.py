
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
    CHAIN_ID = 'CID'
    FAVORITE = False
    LOGO = 'LGO'
    ABI = 'ABI'
