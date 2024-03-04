import web3


def getBalance(address: str, provider: str) -> int:
    w3 = web3.Web3(web3.HTTPProvider(provider))
    address_cksm = web3.Web3.to_checksum_address(address)
    balance = w3.eth.get_balance(address_cksm)
    balance = w3.from_wei(balance, 'ether')
    return balance


def sendTransaction(privateKey: str, sender: str, receiver: str, vale: float, provider: str, chainId: int) -> str:
    txHash = ''
    w3 = web3.Web3(web3.HTTPProvider(provider))
    address_cksm = web3.Web3.to_checksum_address(sender)
    transaction = ({
        'to': receiver,
        'value': w3.to_wei(vale, 'ether'),
        'gas': 2000000,
        'maxFeePerGas': 2000000000,
        'maxPriorityFeePerGas': 1000000000,
        'nonce': w3.eth.get_transaction_count(address_cksm),
        'chainId': chainId})
    """
    ,)
        'type': '0x2',
        # the type is optional and, if omitted, will be interpreted based on the provided transaction parameters
        'accessList': (  # accessList is optional for dynamic fee transactions
            {
                'address': '0xde0b295669a9fd93d5f28d9ec85e40f4cb697bae',
                'storageKeys': (
                    '0x0000000000000000000000000000000000000000000000000000000000000003',
                    '0x0000000000000000000000000000000000000000000000000000000000000007',
                )
            },
            {
                'address': '0xbb9bc244d798123fde783fcc1c72d3bb8c189413',
                'storageKeys': ()
            },)}
    """
    signed = w3.eth.account.sign_transaction(transaction, '0x' + privateKey)
    # print(signed.rawTransaction)
    # print(signed.hash)
    # print(signed.r)
    # print(signed.s)
    # print(signed.v)
    txHash = w3.eth.send_raw_transaction(signed.rawTransaction)
    return txHash.hex()


def getTransaction(txHash: str, provider: str):
    print(txHash)
    tx = ''
    w3 = web3.Web3(web3.HTTPProvider(provider))
    tx = w3.eth.get_transaction(txHash)
    return tx

