from src import network, dataTypes, system, threads, values, ethereum


def readAllTokens(db) -> list:
    try:
        tokens = db.readAllRows(values.TABLE_TOKEN)
        result = []
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


def getAccountTokens(tokens: list, provider: str, address: str) -> list:
    ls = [{}, ]
    t = None
    try:
        for token in tokens:
            t = token
            if token[dataTypes.TOKEN.ABI.value] != 'Null' and token[dataTypes.TOKEN.ABI.value] != 'NOTOK' and token[dataTypes.TOKEN.ADDRESS.value] != 'Null':
                tokenBalance = 0
                try:
                    tokenBalance = ethereum.getTokenBalance(provider=provider,
                                                            contractAddress=token[dataTypes.TOKEN.ADDRESS.value],
                                                            targetAddress=address)
                except Exception as er:
                    print(f">>>{t[dataTypes.TOKEN.NAME.value]} by symbol {t[dataTypes.TOKEN.SYMBOL.value]}\n"
                          f">>>and address {t[dataTypes.TOKEN.ADDRESS.value]}\n"
                          f">>>abi value is {t[dataTypes.TOKEN.ABI.value]}")
                    print(f"getAccountTokens -> {er}")
                    pass
                print(f"{token[dataTypes.TOKEN.SYMBOL.value]} Balance = {tokenBalance}")
                if tokenBalance > 0:
                    ls.append({dataTypes.TOKEN.NAME.value: token[dataTypes.TOKEN.NAME.value],
                               dataTypes.TOKEN.SYMBOL.value: token[dataTypes.TOKEN.ABI.value],
                               dataTypes.TOKEN.LOGO.value: token[dataTypes.TOKEN.LOGO.value],
                               'balance': tokenBalance})
            else:
                print(f">>>{token[dataTypes.TOKEN.NAME.value]} by symbol {token[dataTypes.TOKEN.SYMBOL.value]}\n"
                      f">>>and address {token[dataTypes.TOKEN.ADDRESS.value]}\n"
                      f">>>abi value is {token[dataTypes.TOKEN.ABI.value]}")
        return ls
    except Exception as er:
        print(f">>>{t[dataTypes.TOKEN.NAME.value]} by symbol {t[dataTypes.TOKEN.SYMBOL.value]}\n"
              f">>>and address {t[dataTypes.TOKEN.ADDRESS.value]}\n"
              f">>>abi value is {t[dataTypes.TOKEN.ABI.value]}")
        raise Exception(f"getAccountTokens -> {er}")
