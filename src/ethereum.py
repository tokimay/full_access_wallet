from statistics import median
from urllib import request
from eth_account._utils.legacy_transactions import serializable_unsigned_transaction_from_dict
from eth_account._utils.signing import to_standard_v, extract_chain_id
from web3 import Web3, HTTPProvider


def getBalance(address: str, provider: str) -> int:
    try:
        w3 = Web3(HTTPProvider(provider))
        if not w3.is_connected():
            if not w3.is_connected():
                raise Exception(f"connect to '{provider}' failed.")
        else:
            address_CKSM = Web3.to_checksum_address(address)
            balance = w3.eth.get_balance(address_CKSM)
            return w3.from_wei(balance, 'ether')
    except Exception as er:
        raise Exception(f"getBalance -> {er}")


def estimateGas(txElements: dict) -> dict:
    try:
        BaseFeeMultiplier = {"low": 1,  # 1.10,  # 10% increase
                             "medium": 1.25,  # 1.30,  # 20% increase
                             "high": 1.50  # 1.25  # 25% increase
                             }
        PriorityFeeMultiplier = {"low": 1,  # 1.10, #0.94,  # 6% decrease
                                 "medium": 1.25,  # 1.20, #0.97,  # 3% decrease
                                 "high": 1.50  # 0.98  # 2% decrease
                                 }
        MinimumFee = {"low": 1000000000, "medium": 1500000000, "high": 2000000000}
        priority = {"low": [], "medium": [], "high": []}

        w3 = Web3(HTTPProvider(txElements['provider']))
        if not w3.is_connected():
            raise Exception(f"connect to '{txElements['provider']}' failed.")

        feeHistory = w3.eth.fee_history(50, 'latest', [10, 20, 30])

        for feeList in feeHistory["reward"]:
            # 10 percentile values - low fees
            priority["low"].append(feeList[0])
            # 20 percentile value - medium fees
            priority["medium"].append(feeList[1])
            # 30 percentile value - high fees
            priority["high"].append(feeList[2])

        latestBaseFeePerGas = feeHistory["baseFeePerGas"][-1]

        estimateGasUsed = w3.eth.estimate_gas({'to': Web3.to_checksum_address(txElements['receiver']),
                                               'from': Web3.to_checksum_address(txElements['sender']),
                                               'value': w3.to_wei(txElements['vale'], 'ether'),
                                               'nonce': w3.eth.get_transaction_count(
                                                   Web3.to_checksum_address(txElements['sender'])),
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

            MaxPriorityFeePerGasGwei = round(w3.from_wei(FeeMedian, "gwei"), 6)
            MAXPriorityFee[key] = MaxPriorityFeePerGasGwei

            MaxFeePerGasGwei = round(w3.from_wei((BaseFee + FeeMedian), "gwei"), 6)
            MAX_Fee[key] = MaxFeePerGasGwei

            totalGasFeeGwei = round(w3.from_wei((MaxFeePerGasGwei * estimateGasUsed), "gwei"), 6)
            GasPrice[key] = totalGasFeeGwei
        return {'MAXPriorityFee': MAXPriorityFee, 'MAX_Fee': MAX_Fee, 'GasPrice': GasPrice}
    except Exception as er:
        raise Exception(f"estimateGas -> {er}")


def sendValueTransaction(privateKey: str, txElements: dict) -> str:
    try:
        w3 = Web3(HTTPProvider(txElements['provider']))
        if not w3.is_connected():
            raise Exception(f"connect to '{txElements['provider']}' failed.")
        #print('gas ', w3.to_wei(txElements['GasPrice'], 'ether'), 'wei')
        #print('maxFeePerGas ', w3.to_wei(txElements['maxFeePerGas'], 'ether'), 'wei')
        #print('maxPriorityFeePerGas ', w3.to_wei(txElements['maxFeePerGas'], 'ether'), 'wei')
        transaction = ({
            'to': Web3.to_checksum_address(txElements['receiver']),
            'value': w3.to_wei(txElements['vale'], 'ether'),
            'gas': 200000,  # w3.to_wei(txElements['GasPrice'], 'ether'),
            'maxFeePerGas': 2000000000,  # w3.to_wei(txElements['maxFeePerGas'], 'ether'),
            'maxPriorityFeePerGas': 1000000000,  # w3.to_wei(txElements['MAXPriorityFee'], 'ether'),
            'nonce': w3.eth.get_transaction_count(Web3.to_checksum_address(txElements['sender'])),
            'chainId': txElements['chainId'],
            # 'hardfork': 'petersburg'
        })
        #gas = w3.eth.estimate_gas(transaction)
        #print('gas ', gas)
        #transaction.update({'gas': gas})
        signed = w3.eth.account.sign_transaction(transaction, '0x' + privateKey)
        print('rawTransaction:', signed.rawTransaction)
        print('signed hash:', signed.hash)
        print('r:', signed.r)
        print('s:', signed.s)
        print('v:', signed.v)
        txHash = w3.eth.send_raw_transaction(signed.rawTransaction)
        return txHash.hex()
    except Exception as er:
        raise Exception(f"sendValueTransaction -> {er}")


def getTransaction(txHash: str, provider: str) -> str:
    try:
        w3 = Web3(HTTPProvider(provider))
        if not w3.is_connected():
            raise Exception(f"connect to '{provider}' failed.")

        tx = w3.eth.get_transaction(txHash)
        return Web3.to_json(tx)
    except Exception as er:
        raise Exception(f"getTransaction -> {er}")


def sendMessageTransaction(privateKey: str, txElements: dict) -> str:
    try:
        w3 = Web3(HTTPProvider(txElements['provider']))
        if not w3.is_connected():
            raise Exception(f"connect to '{txElements['provider']}' failed.")
        transaction = ({
            'to': Web3.to_checksum_address(txElements['receiver']),
            'value': w3.to_wei(txElements['vale'], 'ether'),
            'gas': 2000000,
            'maxFeePerGas': 2000000000,
            'maxPriorityFeePerGas': 1000000000,
            'nonce': w3.eth.get_transaction_count(Web3.to_checksum_address(txElements['sender'])),
            'chainId': txElements['chainId'],
            # 'hardfork': 'petersburg',
            'data': txElements['data']
        })
        #gas = w3.eth.estimate_gas(transaction)
        #print('gas ', gas)
        #transaction.update({'gas': gas})
        signed = w3.eth.account.sign_transaction(transaction, '0x' + privateKey)
        print('rawTransaction:', signed.rawTransaction)
        print('signed hash:', signed.hash)
        print('r:', signed.r)
        print('s:', signed.s)
        print('v:', signed.v)
        txHash = w3.eth.send_raw_transaction(signed.rawTransaction)
        return txHash.hex()
    except Exception as er:
        raise Exception(f"sendMessageTransaction -> {er}")


def getAccountNonce(address: str, provider: str) -> int:
    try:
        w3 = Web3(HTTPProvider(provider))
        if not w3.is_connected():
            raise Exception(f"connect to '{provider}' failed.")
        return w3.eth.get_transaction_count(Web3.to_checksum_address(address))
    except Exception as er:
        raise Exception(f"getAccountNonce -> {er}")


def getTransactionHistory(address: str, provider: str, API: str, mainNet: bool, isInternal: bool) -> bytes:
    try:
        w3 = Web3(HTTPProvider(provider))
        if not w3.is_connected():
            raise Exception(f"connect to '{provider}' failed.")
        last = w3.eth.block_number  # get last block number
        if mainNet:
            url = 'https://api.etherscan.io/api'
        else:
            url = 'https://api-sepolia.etherscan.io/api'
        if isInternal:
            action = 'txlistinternal'
        else:
            action = 'txlist'
        target = (f'{url}'
                  '?module=account'
                  f'&action={action}'
                  f'&address={address}'
                  '&startblock=0'
                  f'&endblock={last}'
                  '&page=1'
                  '&offset=10000'
                  '&sort=desc'
                  f'&apikey={API}')
        return request.urlopen(target).read()
    except Exception as er:
        raise Exception(f"getNormalHistory -> {er}")


def getPublicKeyFromTransaction(TXHash: str, provider: str) -> dict:
    try:
        w3 = Web3(HTTPProvider(provider))
        if not w3.is_connected():
            raise Exception(f"connect to '{provider}' failed.")

        tx = w3.eth.get_transaction(TXHash)
        r = tx.r.hex()
        s = tx.s.hex()
        v = (to_standard_v(extract_chain_id(tx.v)[1]))

        print('r: ', r)
        print('s: ', s)
        print('v: ', v)

        sg = w3.eth.account._keys.Signature(vrs=(v, int(r, 16), int(s, 16)))

        tt = {k: tx[k] for k in
              ["to", "nonce", "value", "gas", "chainId", "maxFeePerGas", "maxPriorityFeePerGas", "type", ]}
        tt["data"] = tx["input"]
        ut = serializable_unsigned_transaction_from_dict(tt)
        recover_public_address = sg.recover_public_key_from_msg_hash(ut.hash())
        recover_address = sg.recover_public_key_from_msg_hash(ut.hash()).to_checksum_address()
        return {'publicKey': recover_public_address.to_hex(), 'address': recover_address}
    except Exception as er:
        raise Exception(f"getPublicKeyFromTransaction -> {er}")
