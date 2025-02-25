
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

from json import loads, dumps
from statistics import median
from urllib import request

import web3.middleware
from eth_account._utils.legacy_transactions import serializable_unsigned_transaction_from_dict
from eth_account._utils.signing import to_standard_v, extract_chain_id
from web3 import Web3, HTTPProvider
from time import gmtime, strftime

from src import network, values
from src.validators import checkURI


def getBalance(
        address: str,
        provider: str
) -> float:
    try:
        checkURI(provider)
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


def getTokenBalance(
        provider: str,
        contractAddress: str,
        targetAddress: str,
        abi: list = None
) -> float:
    try:
        checkURI(provider)
        w3 = Web3(HTTPProvider(provider))
        if not w3.is_connected():
            raise Exception(f"connect to '{provider}' failed.")
        if abi is None:
            contract = w3.eth.contract(Web3.to_checksum_address(contractAddress.lower()), abi=values.BASIC_ABI)
        else:
            contract = w3.eth.contract(Web3.to_checksum_address(contractAddress.lower()), abi=abi)
        return contract.functions.balanceOf(Web3.to_checksum_address(targetAddress.lower())).call()
    except Exception as er:
        raise Exception(f"getTokenBalance -> {er} \naddress: {contractAddress}\nprovider: {provider}")


def estimateGas(
        txElements: dict
) -> dict:
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

            MaxPriorityFeePerGasGwei = round(w3.from_wei(FeeMedian, "gwei"), 6)
            MAXPriorityFee[key] = MaxPriorityFeePerGasGwei

            MaxFeePerGasGwei = round(w3.from_wei((BaseFee + FeeMedian), "gwei"), 6)
            MAX_Fee[key] = MaxFeePerGasGwei

            totalGasFeeGwei = round(w3.from_wei((MaxFeePerGasGwei * estimateGasUsed), "gwei"), 6)
            GasPrice[key] = totalGasFeeGwei
        return {'MAXPriorityFee': MAXPriorityFee, 'MAX_Fee': MAX_Fee, 'GasPrice': GasPrice}
    except Exception as er:
        raise Exception(f"estimateGas -> {er}")


def sendValueTransaction(
        privateKey: str,
        txElements: dict,
        duplicate: bool = False
) -> dict:
    result = {'message': '', 'hash': '', 'pending': 0}
    noncePending = 0
    nonceConfirmed = 0
    try:
        checkURI(txElements['provider'])
        w3 = Web3(HTTPProvider(txElements['provider']))
        if not w3.is_connected():
            raise Exception(f"connect to '{txElements['provider']}' failed.")
        gas = int((w3.to_wei(txElements['GasPrice'], 'ether')) / 10000000000)
        if gas < 21000:
            gas = 21000
        maxFeePerGas = int((w3.to_wei(txElements['maxFeePerGas'], 'ether')) / 10000000000)
        maxPriorityFeePerGas = int((w3.to_wei(txElements['maxFeePerGas'], 'ether')) / 10000000000)
        # if maxPriorityFeePerGas < 1000000000:
        #    maxPriorityFeePerGas = 1000000000
        nonceConfirmed = w3.eth.get_transaction_count(Web3.to_checksum_address(txElements['sender']))
        noncePending = w3.eth.get_transaction_count(Web3.to_checksum_address(txElements['sender']),
                                                    'pending')
        if duplicate:
            nonce = noncePending
        else:
            nonce = nonceConfirmed
        print(f"{strftime('%H:%M:%S', gmtime())}: gas {gas} Gwei")
        print(f"{strftime('%H:%M:%S', gmtime())}: maxFeePerGas {maxFeePerGas} Gwei")
        print(f"{strftime('%H:%M:%S', gmtime())}: maxPriorityFeePerGas {maxPriorityFeePerGas} Gwei")
        print(f"{strftime('%H:%M:%S', gmtime())}: nonce {nonce}")

        transaction = ({
            'to': Web3.to_checksum_address(txElements['receiver']),
            'value': w3.to_wei(txElements['vale'], 'ether'),
            'gas': gas,  # 200000,
            'maxFeePerGas': maxFeePerGas,  # 2000000000,
            'maxPriorityFeePerGas': maxPriorityFeePerGas,  # 1000000000,
            'nonce': w3.eth.get_transaction_count(Web3.to_checksum_address(txElements['sender'])),
            'chainId': txElements['chainId'],
            # 'hardfork': 'petersburg'
        })
        estimatedGas = w3.eth.estimate_gas(transaction)
        if gas < estimatedGas:
            gas = estimatedGas
            transaction.update({'gas': gas})
            print(f"{strftime('%H:%M:%S', gmtime())}: new gas {gas} Gwei")
        lastBlockBaseFeePerGas = getPendingBlock(txElements['provider'])['baseFeePerGas']
        if maxFeePerGas < lastBlockBaseFeePerGas:
            maxFeePerGas = lastBlockBaseFeePerGas
            transaction.update({'maxFeePerGas': maxFeePerGas})
            print(f"{strftime('%H:%M:%S', gmtime())}: new maxFeePerGas {maxFeePerGas} Gwei")

        signed = w3.eth.account.sign_transaction(transaction, '0x' + privateKey)
        print(f"{strftime('%H:%M:%S', gmtime())}: rawTransaction: {signed.rawTransaction}")
        print(f"{strftime('%H:%M:%S', gmtime())}: signed hash: {signed.hash.hex()}")
        print(f"{strftime('%H:%M:%S', gmtime())}: r: {signed.r}")
        print(f"{strftime('%H:%M:%S', gmtime())}: s: {signed.s}")
        print(f"{strftime('%H:%M:%S', gmtime())}: v: {signed.v}")
        txHash = w3.eth.send_raw_transaction(signed.rawTransaction)
        result['message'] = 'succeed'
        result['pending'] = noncePending - nonceConfirmed
        result['hash'] = txHash.hex()
    except Exception as er:
        er = str(er).replace("\'", "\"")
        er = loads(er)
        result['message'] = er['message']
        result['pending'] = noncePending - nonceConfirmed
        raise Exception(f"sendValueTransaction -> {er}")
    finally:
        return result


def sendMessageTransaction(
        privateKey: str,
        txElements: dict,
        duplicate: bool = False
) -> dict:
    result = {'message': '', 'hash': '', 'pending': 0}
    noncePending = 0
    nonceConfirmed = 0
    try:
        checkURI(txElements['provider'])
        w3 = Web3(HTTPProvider(txElements['provider']))
        if not w3.is_connected():
            raise Exception(f"connect to '{txElements['provider']}' failed.")
        gas = int((w3.to_wei(txElements['GasPrice'], 'ether')) / 10000000000)
        maxFeePerGas = int((w3.to_wei(txElements['maxFeePerGas'], 'ether')) / 10000000000)
        maxPriorityFeePerGas = int((w3.to_wei(txElements['maxFeePerGas'], 'ether')) / 10000000000)
        # if maxPriorityFeePerGas < 1000000000:
        #    maxPriorityFeePerGas = 1000000000
        nonceConfirmed = w3.eth.get_transaction_count(Web3.to_checksum_address(txElements['sender']))
        noncePending = w3.eth.get_transaction_count(Web3.to_checksum_address(txElements['sender']),
                                                    'pending')
        if duplicate:
            nonce = noncePending
        else:
            nonce = nonceConfirmed
        print(f"{strftime('%H:%M:%S', gmtime())}: gas {gas} Gwei")
        print(f"{strftime('%H:%M:%S', gmtime())}: maxFeePerGas {maxFeePerGas} Gwei")
        print(f"{strftime('%H:%M:%S', gmtime())}: maxPriorityFeePerGas {maxPriorityFeePerGas} Gwei")
        print(f"{strftime('%H:%M:%S', gmtime())}: nonce {nonce}")
        transaction = ({
            'to': Web3.to_checksum_address(txElements['receiver']),
            'value': w3.to_wei(txElements['vale'], 'ether'),
            'gas': gas,  # 200000,
            'maxFeePerGas': maxFeePerGas,  # 2000000000,
            'maxPriorityFeePerGas': maxPriorityFeePerGas,  # 1000000000,
            'nonce': w3.eth.get_transaction_count(Web3.to_checksum_address(txElements['sender'])),
            'chainId': txElements['chainId'],
            # 'hardfork': 'petersburg',
            'data': txElements['data']
        })
        estimatedGas = w3.eth.estimate_gas(transaction)
        if gas < estimatedGas:
            gas = estimatedGas
            transaction.update({'gas': gas})
            print(f"{strftime('%H:%M:%S', gmtime())}: new gas {gas} Gwei")
        lastBlockBaseFeePerGas = getPendingBlock(txElements['provider'])['baseFeePerGas']
        if maxFeePerGas < lastBlockBaseFeePerGas:
            maxFeePerGas = lastBlockBaseFeePerGas
            transaction.update({'maxFeePerGas': maxFeePerGas})
            print(f"{strftime('%H:%M:%S', gmtime())}: new maxFeePerGas {maxFeePerGas} Gwei")

        signed = w3.eth.account.sign_transaction(transaction, '0x' + privateKey)
        print(f"{strftime('%H:%M:%S', gmtime())}: rawTransaction: {signed.rawTransaction}")
        print(f"{strftime('%H:%M:%S', gmtime())}: signed hash: {signed.hash.hex()}")
        print(f"{strftime('%H:%M:%S', gmtime())}: r: {signed.r}")
        print(f"{strftime('%H:%M:%S', gmtime())}: s: {signed.s}")
        print(f"{strftime('%H:%M:%S', gmtime())}: v: {signed.v}")
        txHash = w3.eth.send_raw_transaction(signed.rawTransaction)
        result['message'] = 'succeed'
        result['pending'] = noncePending - nonceConfirmed
        result['hash'] = txHash.hex()
    except Exception as er:
        er = str(er).replace("\'", "\"")
        er = loads(er)
        result['message'] = er['message']
        result['pending'] = noncePending - nonceConfirmed
        raise Exception(f"sendMessageTransaction -> {er}")
    finally:
        return result


def sendTokenTransaction(
        privateKey: str,
        txElements: dict,
        duplicate: bool = False
) -> dict:
    result = {'message': '', 'hash': '', 'pending': 0}
    noncePending = 0
    nonceConfirmed = 0
    try:
        checkURI(txElements['provider'])
        w3 = Web3(HTTPProvider(txElements['provider']))
        if not w3.is_connected():
            raise Exception(f"connect to '{txElements['provider']}' failed.")

        gas = int((w3.to_wei(txElements['GasPrice'], 'ether')) / 10000000000)
        maxFeePerGas = int((w3.to_wei(txElements['maxFeePerGas'], 'ether')) / 10000000000)
        maxPriorityFeePerGas = int((w3.to_wei(txElements['maxFeePerGas'], 'ether')) / 10000000000)
        # if maxPriorityFeePerGas < 1000000000:
        #    maxPriorityFeePerGas = 1000000000
        nonceConfirmed = w3.eth.get_transaction_count(Web3.to_checksum_address(txElements['sender']))
        noncePending = w3.eth.get_transaction_count(Web3.to_checksum_address(txElements['sender']),
                                                    'pending')
        if duplicate:
            nonce = noncePending
        else:
            nonce = nonceConfirmed
        print(f"{strftime('%H:%M:%S', gmtime())}: gas {gas} Gwei")
        print(f"{strftime('%H:%M:%S', gmtime())}: maxFeePerGas {maxFeePerGas} Gwei")
        print(f"{strftime('%H:%M:%S', gmtime())}: maxPriorityFeePerGas {maxPriorityFeePerGas} Gwei")
        print(f"{strftime('%H:%M:%S', gmtime())}: nonce {nonce}")
        if txElements['abi'] is None:
            contract = w3.eth.contract(Web3.to_checksum_address(txElements['contractAddress'].lower()),
                                       abi=getABI(txElements['contractAddress']))
        else:
            contract = w3.eth.contract(Web3.to_checksum_address(txElements['contractAddress'].lower()),
                                       abi=txElements['abi'])
        contract_call = contract.functions.transfer(
            Web3.to_checksum_address(txElements['receiver']),
            w3.to_wei(float(txElements['vale']), 'ether')
        )
        transaction = contract_call.build_transaction(
            {
                'gas': gas,  # 200000,
                'maxFeePerGas': maxFeePerGas,  # 2000000000,
                'maxPriorityFeePerGas': maxPriorityFeePerGas,  # 1000000000,
                'nonce': w3.eth.get_transaction_count(Web3.to_checksum_address(txElements['sender'])),
                'chainId': txElements['chainId']
                # 'hardfork': 'petersburg',
                # 'data': txElements['data']
             })
        print(77)
        signed = w3.eth.account.sign_transaction(transaction, '0x' + privateKey)
        print(f"{strftime('%H:%M:%S', gmtime())}: rawTransaction: {signed.rawTransaction}")
        print(f"{strftime('%H:%M:%S', gmtime())}: signed hash: {signed.hash.hex()}")
        print(f"{strftime('%H:%M:%S', gmtime())}: r: {signed.r}")
        print(f"{strftime('%H:%M:%S', gmtime())}: s: {signed.s}")
        print(f"{strftime('%H:%M:%S', gmtime())}: v: {signed.v}")
        txHash = w3.eth.send_raw_transaction(signed.rawTransaction)
        result['message'] = 'succeed'
        result['pending'] = noncePending - nonceConfirmed
        result['hash'] = txHash.hex()
    except Exception as er:
        er = str(er).replace("\'", "\"")
        er = loads(er)
        result['message'] = er['message']
        result['pending'] = noncePending - nonceConfirmed
        raise Exception(f"sendTokenTransaction -> {er}")
    finally:
        return result


def getTransaction(
        txHash: str,
        provider: str
) -> str:
    try:
        checkURI(provider)
        w3 = Web3(HTTPProvider(provider))
        if not w3.is_connected():
            raise Exception(f"connect to '{provider}' failed.")

        tx = w3.eth.get_transaction(txHash)
        return Web3.to_json(tx)
    except Exception as er:
        raise Exception(f"getTransaction -> {er}")


def getAccountNonce(
        address: str,
        provider: str
) -> int:
    try:
        checkURI(provider)
        w3 = Web3(HTTPProvider(provider))
        if not w3.is_connected():
            raise Exception(f"connect to '{provider}' failed.")
        return w3.eth.get_transaction_count(Web3.to_checksum_address(address))
    except Exception as er:
        raise Exception(f"getAccountNonce -> {er}")


def getTransactionHistory(
        address: str,
        provider: str,
        API: str,
        mainNet: bool,
        isInternal: bool
) -> bytes:
    try:
        checkURI(provider)
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


def getPublicKeyFromTransaction(
        TXHash: str,
        provider: str
) -> dict:
    try:
        checkURI(provider)
        w3 = Web3(HTTPProvider(provider))
        if not w3.is_connected():
            raise Exception(f"connect to '{provider}' failed.")

        tx = w3.eth.get_transaction(TXHash)
        r = tx.r.hex()
        s = tx.s.hex()
        v = (to_standard_v(extract_chain_id(tx.v)[1]))

        print(f"{strftime('%H:%M:%S', gmtime())}: r: {r}")
        print(f"{strftime('%H:%M:%S', gmtime())}: s: {s}")
        print(f"{strftime('%H:%M:%S', gmtime())}: v: {v}")

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


def getPendingTransactions(
        provider: str
) -> list:
    checkURI(provider)
    return getPendingBlock(provider)['transactions']


def getLastBlock(
        provider: str
) -> dict:
    try:
        checkURI(provider)
        w3 = Web3(HTTPProvider(provider))
        if not w3.is_connected():
            raise Exception(f"connect to '{provider}' failed.")
        lastBlock = w3.eth.get_block("latest")
        lastBlock = Web3.to_json(lastBlock)
        return loads(lastBlock)
    except Exception as er:
        raise Exception(f"getLastBlock -> {er}")


def getPendingBlock(
        provider: str
) -> dict:
    try:
        checkURI(provider)
        w3 = Web3(HTTPProvider(provider))
        if not w3.is_connected():
            raise Exception(f"connect to '{provider}' failed.")
        pendingBlock = w3.eth.get_block("pending")
        pendingBlock = Web3.to_json(pendingBlock)
        return loads(pendingBlock)
    except Exception as er:
        raise Exception(f"getLastBlock -> {er}")


def getABI(
        contractAddress: str
) -> str:
    try:
        response = network.getRequest(f"https://api.etherscan.io/api?module=contract&action=getabi&address="
                                      f"{contractAddress}")
        response_json = response.json()
        abi_json = loads(response_json['result'])
        return dumps(abi_json, indent=4, sort_keys=True)
    except Exception as er:
        raise Exception(f"getABI -> {er}")


def getTokenInfo(
        provider: str,
        contractAddress: str
) -> dict:
    try:
        checkURI(provider)
        w3 = Web3(HTTPProvider(provider))
        if not w3.is_connected():
            raise Exception(f"connect to '{provider}' failed.")
        abi = getABI(contractAddress)
        contract = w3.eth.contract(Web3.to_checksum_address(contractAddress.lower()), abi=abi)
        return {
            'address': contractAddress,
            'api': abi,
            'name': contract.functions.name().call(),
            'symbol': contract.functions.symbol().call(),
            'decimals': contract.functions.decimals().call()
        }
    except Exception as er:
        raise Exception(f"getTokenInfo -> {er}")
