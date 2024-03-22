from src import network, dataTypes, system, threads, values, ethereum


def readAllTokens(db) -> list:
    try:
        tokens = db.readAllRows(values.TABLE_TOKEN)
        result =[]
        for token in tokens:
            d = {
                dataTypes.TOKEN.NAME.value: token[0],
                dataTypes.TOKEN.ADDRESS.value: token[1],
                dataTypes.TOKEN.SYMBOL.value: token[2],
                dataTypes.TOKEN.TYPE.value: token[3],
                dataTypes.TOKEN.DECIMALS.value: token[4],
                dataTypes.TOKEN.LOGO.value: token[5],
                dataTypes.TOKEN.ABI.value: token[6]
            }
            result.append(d)
        return result
    except Exception as er:
        raise Exception(f"readTokens -> {er}")


def getAccountTokens(db, provider: str, address: str):
    t = None
    try:
        tokens = readAllTokens(db)
        for token in tokens:
            t = token
            if token['ABI'] != 'Null' and token['ABI'] != 'NOTOK' and token['ADR'] != 'Null':
                tokenBalance = ethereum.getTokenBalance(provider=provider, contractAddress=token['ADR'],
                                                        abi=token['ABI'], targetAddress=address)
                print(f"{token['SYM']} Balance = {tokenBalance}")
            else:
                print(f">>>{token['NAM']} by symbol {token['SYM']}\n"
                      f">>>and address {token['NAM']}\n"
                      f">>>abi value is {token['ABI']}")
    except Exception as er:
        print(f">>>{t['NAM']} by symbol {t['SYM']}\n"
              f">>>and address {t['NAM']}\n"
              f">>>abi value is {t['ABI']}")
        raise Exception(f"getAccountTokens -> {er}")
