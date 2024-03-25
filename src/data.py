from src import network, dataTypes, system, threads, values, ethereum
from time import gmtime, strftime


def readAllFavoriteTokens(db) -> list:
    try:
        tokens = db.readAllRowsByCondition(values.TABLE_TOKEN, dataTypes.TOKEN.FAVORITE.value, True)
        result = []
        for token in tokens:
            d = {
                dataTypes.TOKEN.NAME.value: token[0],
                dataTypes.TOKEN.ADDRESS.value: token[1],
                dataTypes.TOKEN.SYMBOL.value: token[2],
                dataTypes.TOKEN.TYPE.value: token[3],
                dataTypes.TOKEN.DECIMALS.value: token[4],
                dataTypes.TOKEN.FAVORITE.value: token[5],
                dataTypes.TOKEN.LOGO.value: token[6],
                dataTypes.TOKEN.ABI.value: token[7]
            }
            result.append(d)
        return result
    except Exception as er:
        raise Exception(f"readAllFavoriteTokens -> {er}")


"""
def getAccountTokens(tokens: list, provider: str, address: str) -> list:
    ls = []
    t = None
    try:
        for token in tokens:
            t = token
            if token[dataTypes.TOKEN.FAVORITE.value]:  # if it is favorite
                if token[dataTypes.TOKEN.ABI.value] != 'Null' and token[dataTypes.TOKEN.ABI.value] != 'NOTOK' and token[
                    dataTypes.TOKEN.ADDRESS.value] != 'Null':
                    tokenBalance = 0
                    try:
                        tokenBalance = ethereum.getTokenBalance(provider=provider,
                                                                contractAddress=token[dataTypes.TOKEN.ADDRESS.value],
                                                                targetAddress=address)
                    except Exception as er:
                        print(
                            f"{strftime('%H:%M:%S', gmtime())}:>>>{t[dataTypes.TOKEN.NAME.value]} by symbol {t[dataTypes.TOKEN.SYMBOL.value]}\n"
                            f"{strftime('%H:%M:%S', gmtime())}:>>>and address {t[dataTypes.TOKEN.ADDRESS.value]}\n"
                            f"{strftime('%H:%M:%S', gmtime())}:>>>abi value is {t[dataTypes.TOKEN.ABI.value]}")
                        print(f"{strftime('%H:%M:%S', gmtime())}:getAccountTokens -> {er}")
                        pass
                    print(f"{strftime('%H:%M:%S', gmtime())}:{token[dataTypes.TOKEN.SYMBOL.value]} "
                          f"Balance = {tokenBalance}")
                    ls.append({dataTypes.TOKEN.NAME.value: token[dataTypes.TOKEN.NAME.value],
                               dataTypes.TOKEN.SYMBOL.value: token[dataTypes.TOKEN.SYMBOL.value],
                               dataTypes.TOKEN.ADDRESS.value: token[dataTypes.TOKEN.ADDRESS.value],
                               dataTypes.TOKEN.LOGO.value: token[dataTypes.TOKEN.LOGO.value],
                               'balance': tokenBalance})
                else:
                    print(
                        f"{strftime('%H:%M:%S', gmtime())}:>>>{token[dataTypes.TOKEN.NAME.value]} by symbol {token[dataTypes.TOKEN.SYMBOL.value]}\n"
                        f"{strftime('%H:%M:%S', gmtime())}:>>>and address {token[dataTypes.TOKEN.ADDRESS.value]}\n"
                        f"{strftime('%H:%M:%S', gmtime())}:>>>abi value is {token[dataTypes.TOKEN.ABI.value]}")
        #  add ETH at end
        ls.append({dataTypes.TOKEN.NAME.value: 'Ethereum',
                   dataTypes.TOKEN.SYMBOL.value: 'ETH',
                   dataTypes.TOKEN.ADDRESS.value: 'Null',
                   dataTypes.TOKEN.LOGO.value: 'https://raw.githubusercontent.com/tokimay/Full_Access_Wallet/'
                                               'main/resources/tokensLogo/ETH.jpg',
                   'balance': 0})
        return ls
    except Exception as er:
        print(
            f"{strftime('%H:%M:%S', gmtime())}:>>>{t[dataTypes.TOKEN.NAME.value]} by symbol {t[dataTypes.TOKEN.SYMBOL.value]}\n"
            f"{strftime('%H:%M:%S', gmtime())}:>>>and address {t[dataTypes.TOKEN.ADDRESS.value]}\n"
            f"{strftime('%H:%M:%S', gmtime())}:>>>abi value is {t[dataTypes.TOKEN.ABI.value]}")
        raise Exception(f"{strftime('%H:%M:%S', gmtime())}:getAccountTokens -> {er}")

"""


def getCoinBalance(data: dict) -> tuple[float, str]:
    try:
        if data['coinsData'][0] == 'Ethereum':
            balance = ethereum.getBalance(data['activeAddress'], data['provider'])
        else:
            balance = ethereum.getTokenBalance(provider=data['provider'],
                                               contractAddress=data['coinsData'][2],
                                               targetAddress=data['activeAddress'])
            balance = balance / 1000000
        return balance, data['coinsData'][1]
    except Exception as er:
        # raise Exception(f"getCoinBalance -> {er}")
        raise Exception(f"{er}")
