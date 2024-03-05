from statistics import median

import web3


def getBalance(address: str, provider: str) -> int:
    w3 = web3.Web3(web3.HTTPProvider(provider))
    print(w3.is_connected())  # returns true, if connected

    address_cksm = web3.Web3.to_checksum_address(address)
    balance = w3.eth.get_balance(address_cksm)
    balance = w3.from_wei(balance, 'ether')
    return balance


def sendTransaction(privateKey: str, txElements: dict) -> str:
    txHash = ''
    w3 = web3.Web3(web3.HTTPProvider(txElements['provider']))
    print(w3.is_connected())  # returns true, if connected

    address_cksm = web3.Web3.to_checksum_address(txElements['sender'])
    transaction = ({
        'to': txElements['receiver'],
        'value': w3.to_wei(txElements['vale'], 'ether'),
        'gas': 2000000,
        'maxFeePerGas': 2000000000,
        'maxPriorityFeePerGas': 1000000000,
        'nonce': w3.eth.get_transaction_count(address_cksm),
        'chainId': txElements['chainId']})
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
    gas = w3.eth.estimate_gas(transaction)
    transaction.update({'gas': gas})

    signed = w3.eth.account.sign_transaction(transaction, '0x' + privateKey)
    # print(signed.rawTransaction)
    # print(signed.hash)
    # print(signed.r)
    # print(signed.s)
    # print(signed.v)
    txHash = w3.eth.send_raw_transaction(signed.rawTransaction)
    return txHash.hex()


def estimateGas(txElements: dict) -> dict:
    BaseFeeMultiplier = {"low": 1, #1.10,  # 10% increase
                         "medium": 1.25, # 1.30,  # 20% increase
                         "high": 1.50 #1.25  # 25% increase
                         }
    PriorityFeeMultiplier = {"low": 1, #1.10, #0.94,  # 6% decrease
                             "medium": 1.25, # 1.20, #0.97,  # 3% decrease
                             "high": 1.50 #0.98  # 2% decrease
                             }
    MinimumFee = {"low": 1000000000, "medium": 1500000000, "high": 2000000000}
    priority = {"low": [], "medium": [], "high": []}

    w3 = web3.Web3(web3.HTTPProvider(txElements['provider']))
    print(w3.is_connected())  # returns true, if connected

    feeHistory = w3.eth.fee_history(10, 'latest', [10, 20, 30])

    for feeList in feeHistory["reward"]:
        # 10 percentile values - low fees
        priority["low"].append(feeList[0])
        # 20 percentile value - medium fees
        priority["medium"].append(feeList[1])
        # 30 percentile value - high fees
        priority["high"].append(feeList[2])

    latestBaseFeePerGas = feeHistory["baseFeePerGas"][-1]

    estimateGasUsed = w3.eth.estimate_gas({'to': web3.Web3.to_checksum_address(txElements['receiver']),
                                           'from': web3.Web3.to_checksum_address(txElements['sender']),
                                           'value': w3.to_wei(txElements['vale'], 'ether'),
                                           'nonce': w3.eth.get_transaction_count(
                                               web3.Web3.to_checksum_address(txElements['sender'])),
                                           'chainId': txElements['chainId']
                                           })

    MAXPriorityFee = {}
    MAX_Fee = {}
    GasPrice = {}
    for key in priority:
        BaseFee = latestBaseFeePerGas * BaseFeeMultiplier[key]

        FeeMedian = (median(priority[key]) * PriorityFeeMultiplier[key])
        # if median fee is less than minimum fee
        if FeeMedian > MinimumFee[key]:
            FeeMedian = MinimumFee[key]

        MaxPriorityFeePerGasGwei = round(w3.from_wei(FeeMedian, "gwei"), 4)
        MAXPriorityFee[key] = MaxPriorityFeePerGasGwei

        MaxFeePerGasGwei = round(w3.from_wei((BaseFee + FeeMedian), "gwei"), 4)
        MAX_Fee[key] = MaxFeePerGasGwei

        totalGasFeeGwei = round(w3.from_wei((MaxFeePerGasGwei * estimateGasUsed), "gwei"), 4)
        GasPrice[key] = totalGasFeeGwei

    return {'MAXPriorityFee': MAXPriorityFee, 'MAX_Fee': MAX_Fee, 'GasPrice': GasPrice}


def getTransaction(txHash: str, provider: str):
    print(txHash)
    tx = ''
    w3 = web3.Web3(web3.HTTPProvider(provider))
    print(w3.is_connected())  # returns true, if connected

    tx = w3.eth.get_transaction(txHash)
    return tx
