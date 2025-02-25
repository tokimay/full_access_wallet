
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

from requests import get
from sha3 import keccak_256
from src import values, dataTypes, cryptography, ellipticCurve, validators
from src.GUI import gui_mouseTracker


"""
ETHEREUM_DEFAULT_PATH = "m/44'/60'/0'/0/0"
"""

LEN_ENTROPY = 256
LEN_CEK_SM_ENTROPY = 256 + 8
LEN_SHA256_ENTROPY = 256
LEN_PRIVATE_KEY = 64
LEN_PUBLIC_KEY = 128
LEN_BIP39 = 2048
LEN_MNEMONIC = 24


class New:
    def __init__(self):
        pass

    @staticmethod
    def newEntropy() -> str:
        try:
            mouseTracker = gui_mouseTracker.WINDOW()
            mouseTracker.exec()
            return mouseTracker.getEntropy()
        except Exception as er:
            raise Exception(f"newEntropy -> {er}")

    @staticmethod
    def entropyToPrivateKey(entropy: str) -> str:
        try:
            validators.checkType(entropy, dataTypes.TYPE.STRING)
            if entropy.startswith('0b'):
                entropy = entropy[2:]
            validators.checkLen(entropy, LEN_ENTROPY)
            return cryptography.ENTROPY.ToPbkdf2HmacSha256(entropy)  # need complete by hashing
        except Exception as er:
            raise Exception(f"entropyToPrivateKey -> {er}")

    @staticmethod
    def privateKeyToPublicKeyCoordinate(privateKey: str) -> tuple:
        try:
            validators.checkType(privateKey, dataTypes.TYPE.STRING)
            validators.checkHex(privateKey)
            if privateKey.startswith('0x') or privateKey.startswith('0X'):
                privateKey = privateKey[2:]
            validators.checkLen(privateKey, LEN_PRIVATE_KEY)
            curve = ellipticCurve.secp256k1()
            publicKeyCoordinate = curve.getPublicKeyCoordinate(int(privateKey, 16))
            if not curve:
                raise Exception(f"calculated coordinates are not on the curve.")
            return publicKeyCoordinate
        except Exception as er:
            raise Exception(f"privateKeyToPublicKeyCoordinate -> {er}")

    @staticmethod
    def publicKeyCoordinateToPublicKey(coordinate: tuple) -> str:
        try:
            validators.checkType(coordinate, dataTypes.TYPE.TUPLE)
            validators.checkLen(coordinate, 2)
            coordinate_x_y = (coordinate[0].to_bytes(32, byteorder='big') +
                              coordinate[1].to_bytes(32, byteorder='big'))
            return '0x' + coordinate_x_y.hex()
        except Exception as er:
            raise Exception(f"publicKeyCoordinateToPublicKey -> {er}")

    @staticmethod
    def publicKeyToAddress(publicKey: str) -> str:
        try:
            validators.checkType(publicKey, dataTypes.TYPE.STRING)
            validators.checkHex(publicKey)
            if publicKey.startswith('0x') or publicKey.startswith('0X'):
                publicKey = publicKey[2:]
            validators.checkLen(publicKey, LEN_PUBLIC_KEY)
            return '0x' + keccak_256(bytes.fromhex(publicKey)).digest()[-20:].hex()
        except Exception as er:
            raise Exception(f"publicKeyToAddress -> {er}")

    @staticmethod
    def entropyToMnemonic(entropy: str) -> str:
        try:
            validators.checkType(entropy, dataTypes.TYPE.STRING)
            if entropy.startswith('0b'):
                entropy = entropy[2:]
            validators.checkLen(entropy, LEN_ENTROPY)

            mnemonic = []
            bip39 = get(values.BIP_39_LIST_URI).text.splitlines()

            validators.checkType(bip39, dataTypes.TYPE.LIST)
            validators.checkLen(bip39, LEN_BIP39)

            sha256Entropy = cryptography.ENTROPY.ToSha256(entropy)
            if sha256Entropy.startswith('0b'):
                sha256Entropy = entropy[2:]
            validators.checkLen(sha256Entropy, LEN_SHA256_ENTROPY)

            checkSumEntropy = entropy + str(sha256Entropy[:8])
            validators.checkLen(checkSumEntropy, LEN_CEK_SM_ENTROPY)

            chunk = 11
            while chunk <= LEN_CEK_SM_ENTROPY:
                mnemonic.append(bip39[int(checkSumEntropy[(chunk - 11):chunk], 2)])
                chunk = chunk + 11
            if not len(mnemonic) == LEN_MNEMONIC:
                raise Exception(f"Generating mnemonic failed. Incompatible length received.\n{len(mnemonic)}")
            return ' '.join(mnemonic)
        except Exception as er:
            raise Exception(f"entropyToMnemonic -> {er}")

    @staticmethod
    def mnemonicToEntropy(mnemonic: str) -> str:
        try:
            entropy = ''
            bip39 = get(values.BIP_39_LIST_URI).text.splitlines()
            validators.checkType(bip39, dataTypes.TYPE.LIST)
            validators.checkLen(bip39, LEN_BIP39)
            mnemonicList = mnemonic.split()
            validators.checkLen(mnemonicList, LEN_MNEMONIC)
            for word in mnemonicList:
                if not (word in bip39):
                    raise Exception(f"Invalid Mnemonic.\n'{word}' is not in BIP39 word list")
                else:
                    index = bin(bip39.index(word))[2:].zfill(11)
                    entropy = entropy + index
            validators.checkLen(entropy, LEN_CEK_SM_ENTROPY)
            checkSum = entropy[-8:]
            entropy = entropy[:-8]  # remove checksum
            sha256Entropy = cryptography.ENTROPY.ToSha256(entropy)
            if sha256Entropy.startswith('0b'):
                sha256Entropy = entropy[2:]
            validators.checkLen(sha256Entropy, LEN_SHA256_ENTROPY)
            if not checkSum == str(sha256Entropy[:8]):
                raise Exception(f"Invalid mnemonic.")
            else:
                return entropy
        except Exception as er:
            raise Exception(f"mnemonicToEntropy -> {er}")

    @staticmethod
    def random() -> dict:
        try:
            entropy = New.newEntropy()
            mnemonic = New.entropyToMnemonic(entropy)
            privateKey = New.entropyToPrivateKey(entropy)
            publicKeyCoordinate = New.privateKeyToPublicKeyCoordinate(privateKey)
            publicKey = New.publicKeyCoordinateToPublicKey(publicKeyCoordinate)
            address = New.publicKeyToAddress(publicKey)
            return {
                'name': 'No name',
                'address': address,
                'entropy': entropy,
                'privateKey': privateKey,
                'publicKeyCoordinate': publicKeyCoordinate,
                'publicKey': publicKey,
                'mnemonic': mnemonic
            }
        except Exception as er:
            raise Exception(f"random -> {er}")

    @staticmethod
    def fromEntropy(entropy: str) -> dict:
        try:
            mnemonic = New.entropyToMnemonic(entropy)
            privateKey = New.entropyToPrivateKey(entropy)
            publicKeyCoordinate = New.privateKeyToPublicKeyCoordinate(privateKey)
            publicKey = New.publicKeyCoordinateToPublicKey(publicKeyCoordinate)
            address = New.publicKeyToAddress(publicKey)
            return {
                'name': 'No name',
                'address': address,
                'entropy': entropy,
                'privateKey': privateKey,
                'publicKeyCoordinate': publicKeyCoordinate,
                'publicKey': publicKey,
                'mnemonic': mnemonic
            }
        except Exception as er:
            raise Exception(f"fromEntropy -> {er}")

    @staticmethod
    def fromPrivateKey(privateKey: str) -> dict:
        try:
            entropy = privateKey
            mnemonic = privateKey
            publicKeyCoordinate = New.privateKeyToPublicKeyCoordinate(privateKey)
            publicKey = New.publicKeyCoordinateToPublicKey(publicKeyCoordinate)
            address = New.publicKeyToAddress(publicKey)
            return {
                'name': 'No name',
                'address': address,
                'entropy': entropy,
                'privateKey': privateKey,
                'publicKeyCoordinate': publicKeyCoordinate,
                'publicKey': publicKey,
                'mnemonic': mnemonic
            }
        except Exception as er:
            raise Exception(f"fromPrivateKey -> {er}")

    @staticmethod
    def fromMnemonic(mnemonic: str) -> dict:
        try:
            entropy = New.mnemonicToEntropy(mnemonic)
            privateKey = New.entropyToPrivateKey(entropy)
            publicKeyCoordinate = New.privateKeyToPublicKeyCoordinate(privateKey)
            publicKey = New.publicKeyCoordinateToPublicKey(publicKeyCoordinate)
            address = New.publicKeyToAddress(publicKey)
            return {
                'name': 'No name',
                'address': address,
                'entropy': entropy,
                'privateKey': privateKey,
                'publicKeyCoordinate': publicKeyCoordinate,
                'publicKey': publicKey,
                'mnemonic': mnemonic
            }
        except Exception as er:
            raise Exception(f"fromMnemonic -> {er}")
