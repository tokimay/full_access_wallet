from statistics import median
from urllib import request
from eth_account._utils.legacy_transactions import serializable_unsigned_transaction_from_dict
from eth_account._utils.signing import to_standard_v, extract_chain_id
from src import gui_errorDialog
from web3 import Web3, HTTPProvider
from src.types import TYPE
from src.validators import checkType, checkHex, checkLen, checkURL


def getBalance(address: str, provider: str) -> int:
    try:
        if not checkType('getBalance', address, TYPE.STRING):
            return -1
        if not checkType('getBalance', provider, TYPE.STRING):
            return -1
        if not checkURL('getBalance', provider):
            return -1
        w3 = Web3(HTTPProvider(provider))
        if not w3.is_connected():
            gui_errorDialog.Error('getBalance', f'Connect to {provider} failed.').exec()
            return -1
        else:
            address_CKSM = Web3.to_checksum_address(address)
            balance = w3.eth.get_balance(address_CKSM)
            balance = w3.from_wei(balance, 'ether')
            return balance
    except Exception as er:
        gui_errorDialog.Error('getBalance', str(er)).exec()
        return -1


def sendTransaction(privateKey: str, txElements: dict) -> str:
    try:
        if not checkType('sendTransaction', privateKey, TYPE.STRING):
            return ''
        if not checkType('sendTransaction', txElements, TYPE.DICTIONARY):
            return ''
        if not checkURL('sendTransaction', txElements['provider']):
            return ''
        txHash = ''
        w3 = Web3(HTTPProvider(txElements['provider']))
        if not w3.is_connected():
            gui_errorDialog.Error('sendTransaction',
                                  f"Connect to {txElements['provider']} failed.").exec()
            return ''

        transaction = ({
            'to': Web3.to_checksum_address(txElements['receiver']),
            'value': w3.to_wei(txElements['vale'], 'ether'),
            'gas': 2000000,
            'maxFeePerGas': 2000000000,
            'maxPriorityFeePerGas': 1000000000,
            'nonce': w3.eth.get_transaction_count(Web3.to_checksum_address(txElements['sender'])),
            'chainId': txElements['chainId']})
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
    except Exception as er:
        gui_errorDialog.Error('sendTransaction', str(er)).exec()
        return ''


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
            gui_errorDialog.Error('estimateGas',
                                  f"Connect to {txElements['provider']} failed.").exec()
            return {}

        feeHistory = w3.eth.fee_history(10, 'latest', [10, 20, 30])

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

            MaxPriorityFeePerGasGwei = round(w3.from_wei(FeeMedian, "gwei"), 4)
            MAXPriorityFee[key] = MaxPriorityFeePerGasGwei

            MaxFeePerGasGwei = round(w3.from_wei((BaseFee + FeeMedian), "gwei"), 4)
            MAX_Fee[key] = MaxFeePerGasGwei

            totalGasFeeGwei = round(w3.from_wei((MaxFeePerGasGwei * estimateGasUsed), "gwei"), 4)
            GasPrice[key] = totalGasFeeGwei

        return {'MAXPriorityFee': MAXPriorityFee, 'MAX_Fee': MAX_Fee, 'GasPrice': GasPrice}
    except Exception as er:
        gui_errorDialog.Error('estimateGas', str(er)).exec()
        return {}


def getTransaction(txHash: str, provider: str) -> str:
    try:
        if not checkType('getTransaction', txHash, TYPE.STRING):
            return ''
        if not checkType('getTransaction', provider, TYPE.STRING):
            return ''
        if not checkURL('getTransaction', provider):
            return ''
        w3 = Web3(HTTPProvider(provider))
        if not w3.is_connected():
            gui_errorDialog.Error('getTransaction',f"Connect to {provider} failed.").exec()
            return ''

        tx = w3.eth.get_transaction(txHash)
        return Web3.to_json(tx)
    except Exception as er:
        gui_errorDialog.Error('getTransaction', str(er)).exec()
        return ''


def getAccountNonce(address: str, provider: str) -> int:
    try:
        if not checkType('getAccountNonce', address, TYPE.STRING):
            return -1
        if not checkType('getAccountNonce', provider, TYPE.STRING):
            return -1
        if not checkURL('getAccountNonce', provider):
            return -1
        w3 = Web3(HTTPProvider(provider))
        if not w3.is_connected():
            gui_errorDialog.Error('getAccountNonce', f"Connect to {provider} failed.").exec()
            return -1
        else:
            count = w3.eth.get_transaction_count(Web3.to_checksum_address(address))
            return count
    except Exception as er:
        gui_errorDialog.Error('getAccountNonce', str(er)).exec()
        return -1


def getNormalHistory(address: str, provider: str, API: str, mainNet: bool) -> bytes:
    try:
        if not checkType('getNormalHistory', address, TYPE.STRING):
            return b''
        if not checkType('getNormalHistory', provider, TYPE.STRING):
            return b''
        if not checkURL('getNormalHistory', provider):
            return b''
        if not checkType('getNormalHistory', API, TYPE.STRING):
            return b''
        if not checkType('getInternalHistory', mainNet, TYPE.BOOLEAN):
            return b''
        w3 = Web3(HTTPProvider(provider))
        if not w3.is_connected():
            gui_errorDialog.Error('getNormalHistory', f"Connect to {provider} failed.").exec()
            return b''
        else:
            last = w3.eth.block_number  # get last block number
            if mainNet:
                url = 'https://api.etherscan.io/api'
            else:
                url = 'https://api-sepolia.etherscan.io/api'
            target = (f'{url}'
                      '?module=account'
                      '&action=txlist'
                      f'&address={address}'
                      '&startblock=0'
                      f'&endblock={last}'
                      '&page=1'
                      '&offset=10000'
                      '&sort=desc'
                      f'&apikey={API}')
            contents = request.urlopen(target).read()
            return contents
    except Exception as er:
        gui_errorDialog.Error('getNormalHistory', str(er)).exec()
        return b''


def getInternalHistory(address: str, provider: str, API: str, mainNet: bool) -> bytes:
    try:
        if not checkType('getInternalHistory', address, TYPE.STRING):
            return b''
        if not checkType('getInternalHistory', provider, TYPE.STRING):
            return b''
        if not checkURL('getInternalHistory', provider):
            return b''
        if not checkType('getInternalHistory', API, TYPE.STRING):
            return b''
        if not checkType('getInternalHistory', mainNet, TYPE.BOOLEAN):
            return b''
        w3 = Web3(HTTPProvider(provider))
        if not w3.is_connected():
            gui_errorDialog.Error('getNormalHistory', f"Connect to {provider} failed.").exec()
            return b''
        else:
            last = w3.eth.block_number  # get last block number
            if mainNet:
                url = 'https://api.etherscan.io/api'
            else:
                url = 'https://api-sepolia.etherscan.io/api'
            target = (f'{url}'
                      '?module=account'
                      '&action=txlistinternal'
                      f'&address={address}'
                      '&startblock=0'
                      f'&endblock={last}'
                      '&page=1'
                      '&offset=10000'
                      '&sort=desc'
                      f'&apikey={API}')
            contents = request.urlopen(target).read()
            return contents
    except Exception as er:
        gui_errorDialog.Error('getInternalHistory', str(er)).exec()
        return b''


def getPublicKeyFromTransaction(TXHash: str, provider: str) -> dict:
    try:
        if not checkType('getPublicKeyFromTransaction', TXHash, TYPE.STRING):
            return {}
        if not checkType('getPublicKeyFromTransaction', provider, TYPE.STRING):
            return {}
        if not checkURL('getPublicKeyFromTransaction', provider):
            return {}
        w3 = Web3(HTTPProvider(provider))
        if not w3.is_connected():
            gui_errorDialog.Error('getPublicKeyFromTransaction', f"Connect to {provider} failed.").exec()
            return {}
        else:
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
        gui_errorDialog.Error('getPublicKeyFromTransaction', str(er)).exec()
        return {}
