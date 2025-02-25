
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


def checkURI(value: str):
    try:
        checkType(value, TYPE.STRING)
        result = urlparse(value)
        return all([result.scheme, result.netloc])
    except Exception as er:
        raise Exception(f"checkURI -> {er}")
