
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

import requests
from src.validators import checkURI
from src.values import *


def getRequest(uri: str):
    try:
        checkURI(uri)
        result = requests.get(uri)
        return result
    except Exception as er:
        raise Exception(f"getRequest -> {er}")


def getTokenList() -> dict:
    try:
        tokes = {"list": []}
        tokenJson = getRequest(TOKEN_LIST_URI)
        for token in tokenJson.json()['list']:
            tokes['list'].append(token)
        return tokes
    except Exception as er:
        raise Exception(f"addTokensList -> {er}")

