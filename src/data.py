
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

from src import network, dataTypes, system, threads, values, ethereum
from time import gmtime, strftime


def readAllFavoriteTokens(db) -> list:
    try:
        tokens = db.readAllRowsByCondition(values.TABLE_TOKEN, dataTypes.TOKEN.FAVORITE.value, True)
        result = []
        for token in tokens:
            d = {
                dataTypes.TOKEN.NAME.value: token[0],  # NAME
                dataTypes.TOKEN.ADDRESS.value: token[1],  # ADDRESS
                dataTypes.TOKEN.SYMBOL.value: token[2],  # SYMBOL
                dataTypes.TOKEN.TYPE.value: token[3],  # TYPE
                dataTypes.TOKEN.DECIMALS.value: token[4],  # DECIMALS
                dataTypes.TOKEN.CHAIN_ID.value: token[5],  # CHAIN_ID
                dataTypes.TOKEN.FAVORITE.value: token[6],  # FAVORITE
                dataTypes.TOKEN.LOGO.value: token[7],  # LOGO
                dataTypes.TOKEN.ABI.value: token[8]  # ABI
            }
            result.append(d)
        return result
    except Exception as er:
        raise Exception(f"readAllFavoriteTokens -> {er}")


def getCoinBalance(data: dict) -> tuple[float, str]:
    try:
        if data['coinsData'][0] == 'Ethereum':
            balance = ethereum.getBalance(data['activeAddress'], data['provider'])
        else:
            balance = ethereum.getTokenBalance(provider=data['provider'],
                                               contractAddress=data['coinsData'][2],
                                               targetAddress=data['activeAddress'])
            balance = balance / 1000000000000000000
        return balance, data['coinsData'][1]
    except Exception as er:
        # raise Exception(f"getCoinBalance -> {er}")
        raise Exception(f"{er}")


def getTokenInfo(coinsList: list, token: str) -> tuple[str, list, int]:
    try:
        contractAddress = ''
        abi = []
        chainID = 0
        exist = False
        for coin in coinsList:
            if coin[dataTypes.TOKEN.NAME.value] == token:
                contractAddress = coin[dataTypes.TOKEN.ADDRESS.value]
                abi = coin[dataTypes.TOKEN.ABI.value]
                chainID = coin[dataTypes.TOKEN.CHAIN_ID.value]
                exist = True
        if exist:
            return contractAddress, abi, chainID
        else:
            raise Exception(f"{token} is not in your token list!")
    except Exception as er:
        raise Exception(f"getTokenInfo -> {er}")
