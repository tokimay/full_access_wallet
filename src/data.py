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
            print(coin)
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
