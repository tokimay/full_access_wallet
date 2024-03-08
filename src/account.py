from json import loads

import requests

from src import gui_errorDialog, gui_mouseTracker
from src.ellipticCurve import secp256k1
from sha3 import keccak_256
from src.encrypt import entropyToSha256, entropyToPbkdf2HmacSha256
from src.types import TYPE
from src.validators import checkType, checkHex, checkLen

"""
ETHEREUM_DEFAULT_PATH = "m/44'/60'/0'/0/0"
"""


class New:
    def __init__(self):
        pass

    @staticmethod
    def newEntropy() -> str:
        try:
            mouseTracker = gui_mouseTracker.UI()
            mouseTracker.exec()
            return mouseTracker.getEntropy()
        except Exception as er:
            gui_errorDialog.Error('newEntropy', str(er)).exec()
            return ''

    @staticmethod
    def entropyToPrivateKey(entropy: str) -> str:
        try:
            if not checkType('entropyToPrivateKey', entropy, TYPE.STRING):
                return ''
            if entropy.startswith('0b'):
                entropy = entropy[2:]
            if not checkLen('entropyToPrivateKey', entropy, 256):
                return ''
            else:
                return entropyToPbkdf2HmacSha256(entropy)  # need complete by hashing
        except Exception as er:
            gui_errorDialog.Error('entropyToPrivateKey', str(er)).exec()
            return ''

    @staticmethod
    def privateKeyToPublicKeyCoordinate(privateKey: str) -> tuple:
        try:
            if not checkType('privateKeyToPublicKeyCoordinate', privateKey, TYPE.STRING):
                return ()
            if not checkHex('privateKeyToPublicKeyCoordinate', privateKey):
                return ()
            if privateKey.startswith('0x') or privateKey.startswith('0X'):
                privateKey = privateKey[2:]
            if not checkLen('entropyToPrivateKey', privateKey, 64):
                return ()
            else:
                curve = secp256k1()
                publicKeyCoordinate = curve.getPublicKeyCoordinate(int(privateKey, 16))
                if len(publicKeyCoordinate) <= 0:
                    gui_errorDialog.Error('privateKeyToPublicKeyCoordinate',
                                          'Getting coordinate from elliptic curve failed.').exec()
                    return ()
                else:
                    return publicKeyCoordinate
        except Exception as er:
            gui_errorDialog.Error('privateKeyToPublicKeyCoordinate', str(er)).exec()
            return ()

    @staticmethod
    def publicKeyCoordinateToPublicKey(coordinate: tuple) -> str:
        try:
            if not checkType('publicKeyCoordinateToPublicKey', coordinate, TYPE.TUPLE):
                return ''
            if len(coordinate) == 0:
                gui_errorDialog.Error('publicKeyCoordinateToPublicKey',
                                      'Coordinate with length 0 is not calculable.').exec()
                return ''
            else:
                coordinate_x_y = (coordinate[0].to_bytes(32, byteorder='big') +
                                  coordinate[1].to_bytes(32, byteorder='big'))
                return '0x' + coordinate_x_y.hex()
        except Exception as er:
            gui_errorDialog.Error('publicKeyCoordinateToPublicKey', str(er)).exec()
            return ''

    @staticmethod
    def publicKeyToAddress(publicKey: str) -> str:
        try:
            if not checkType('publicKeyToAddress', publicKey, TYPE.STRING):
                return ''
            if not checkHex('publicKeyToAddress', publicKey):
                return ''
            if publicKey.startswith('0x') or publicKey.startswith('0X'):
                publicKey = publicKey[2:]
            if not checkLen('publicKeyToAddress', publicKey, 128):
                return ''
            else:
                return '0x' + keccak_256(bytes.fromhex(publicKey)).digest()[-20:].hex()
        except Exception as er:
            gui_errorDialog.Error('publicKeyToAddress', str(er)).exec()
            return ''

    @staticmethod
    def entropyToMnemonic(entropy: str) -> str:
        try:
            if not checkType('entropyToMnemonic', entropy, TYPE.STRING):
                return ''
            if entropy.startswith('0b'):
                entropy = entropy[2:]
            if not checkLen('entropyToMnemonic', entropy, 256):
                return ''
            else:
                mnemonic = []
                response = requests.get(
                    'https://github.com/tokimay/Full_Access_Wallet/blob/main/resources/bip39EnglishWordList.txt')
                file = loads(response.text)
                bip39 = file["payload"]['blob']['rawLines']
                if not checkType('entropyToMnemonic', bip39, TYPE.LIST):
                    return ''
                if not checkLen('entropyToMnemonic', bip39, 2048):
                    return ''
                sha256Entropy = entropyToSha256(entropy)
                if sha256Entropy.startswith('0b'):
                    sha256Entropy = entropy[2:]
                if not checkLen('entropyToMnemonic', sha256Entropy, 256):
                    return ''
                else:
                    checkSumEntropy = entropy + str(sha256Entropy[:8])
                    if not checkLen('entropyToMnemonic', checkSumEntropy, 264):
                        return ''
                    else:
                        chunk = 11
                        while chunk <= 264:
                            mnemonic.append(bip39[int(checkSumEntropy[(chunk - 11):chunk], 2)])
                            chunk = chunk + 11
                        if not len(mnemonic) == 24:
                            gui_errorDialog.Error('entropyToMnemonic',
                                                  f'Generating mnemonic failed.\n'
                                                  f'Incompatible length received.\n'
                                                  f'{len(mnemonic)}').exec()
                            return ''
                        else:
                            return ' '.join(mnemonic)
        except Exception as er:
            gui_errorDialog.Error('entropyToMnemonic', str(er)).exec()
            return ''

    @staticmethod
    def mnemonicToEntropy(mnemonic: str) -> str:
        try:
            entropy = ''
            response = requests.get(
                'https://github.com/tokimay/Full_Access_Wallet/blob/main/resources/bip39EnglishWordList.txt')
            file = loads(response.text)
            bip39 = file["payload"]['blob']['rawLines']
            if not checkType('entropyToMnemonic', bip39, TYPE.LIST):
                return ''
            if not checkLen('entropyToMnemonic', bip39, 2048):
                return ''
            mnemonicList = mnemonic.split()
            if not checkLen('mnemonicToEntropy', mnemonicList, 24):
                return ''
            else:
                for word in mnemonicList:
                    if not (word in bip39):
                        gui_errorDialog.Error('mnemonicToEntropy',
                                              f'Invalid Mnemonic.\n'
                                              f'{word} is not in BIP39 word list').exec()
                        return ''
                    else:
                        index = bin(bip39.index(word))[2:].zfill(11)
                        entropy = entropy + index
                if not checkLen('mnemonicToEntropy', entropy, 264):
                    return ''
                else:
                    checkSum = entropy[-8:]
                    entropy = entropy[:-8]  # remove checksum
                    sha256Entropy = entropyToSha256(entropy)
                    if sha256Entropy.startswith('0b'):
                        sha256Entropy = entropy[2:]
                    if not checkLen('mnemonicToEntropy', sha256Entropy, 256):
                        return ''
                    if not checkSum == str(sha256Entropy[:8]):
                        gui_errorDialog.Error('mnemonicToEntropy', 'Invalid mnemonic.').exec()
                        return ''
                    else:
                        return entropy
        except Exception as er:
            gui_errorDialog.Error('mnemonicToEntropy', str(er)).exec()
            return ''

    @staticmethod
    def random() -> dict:
        try:
            entropy = New.newEntropy()
            print('=', 1)
            if entropy == '':
                return {}
            print('=', 2)
            mnemonic = New.entropyToMnemonic(entropy)
            if mnemonic == '':
                return {}
            print('=', 3)
            privateKey = New.entropyToPrivateKey(entropy)
            if privateKey == '':
                return {}
            print('=', 4)
            publicKeyCoordinate = New.privateKeyToPublicKeyCoordinate(privateKey)
            if publicKeyCoordinate == ():
                return {}
            print('=', 5)
            publicKey = New.publicKeyCoordinateToPublicKey(publicKeyCoordinate)
            if publicKey == '':
                return {}
            print('=', 6)
            address = New.publicKeyToAddress(publicKey)
            if address == '':
                return {}
            print('=', 7)
            return {'entropy': entropy,
                    'privateKey': privateKey,
                    'publicKeyCoordinate': publicKeyCoordinate,
                    'publicKey': publicKey,
                    'address': address,
                    'mnemonic': mnemonic}
        except Exception as er:
            gui_errorDialog.Error('random', str(er)).exec()
            return {}

    @staticmethod
    def fromEntropy(entropy: str) -> dict:
        try:
            mnemonic = New.entropyToMnemonic(entropy)
            if mnemonic == '':
                return {}
            privateKey = New.entropyToPrivateKey(entropy)
            if privateKey == '':
                return {}
            publicKeyCoordinate = New.privateKeyToPublicKeyCoordinate(privateKey)
            if publicKeyCoordinate == ():
                return {}
            publicKey = New.publicKeyCoordinateToPublicKey(publicKeyCoordinate)
            if publicKey == '':
                return {}
            address = New.publicKeyToAddress(publicKey)
            if address == '':
                return {}
            return {'entropy': entropy,
                    'privateKey': privateKey,
                    'publicKeyCoordinate': publicKeyCoordinate,
                    'publicKey': publicKey,
                    'address': address,
                    'mnemonic': mnemonic}
        except Exception as er:
            gui_errorDialog.Error('fromEntropy', str(er)).exec()
            return {}

    @staticmethod
    def fromPrivateKey(privateKey: str) -> dict:
        try:
            entropy = privateKey
            mnemonic = privateKey
            publicKeyCoordinate = New.privateKeyToPublicKeyCoordinate(privateKey)
            if publicKeyCoordinate == ():
                return {}
            publicKey = New.publicKeyCoordinateToPublicKey(publicKeyCoordinate)
            if publicKey == '':
                return {}
            address = New.publicKeyToAddress(publicKey)
            if address == '':
                return {}
            return {'entropy': entropy,
                    'privateKey': privateKey,
                    'publicKeyCoordinate': publicKeyCoordinate,
                    'publicKey': publicKey,
                    'address': address,
                    'mnemonic': mnemonic}
        except Exception as er:
            gui_errorDialog.Error('fromPrivateKey', str(er)).exec()
            return {}

    @staticmethod
    def fromMnemonic(mnemonic: str) -> dict:
        try:
            entropy = New.mnemonicToEntropy(mnemonic)
            print(entropy)
            if entropy == '':
                return {}
            privateKey = New.entropyToPrivateKey(entropy)
            if privateKey == '':
                return {}
            publicKeyCoordinate = New.privateKeyToPublicKeyCoordinate(privateKey)
            if publicKeyCoordinate == ():
                return {}
            publicKey = New.publicKeyCoordinateToPublicKey(publicKeyCoordinate)
            if publicKey == '':
                return {}
            address = New.publicKeyToAddress(publicKey)
            if address == '':
                return {}
            return {'entropy': entropy,
                    'privateKey': privateKey,
                    'publicKeyCoordinate': publicKeyCoordinate,
                    'publicKey': publicKey,
                    'address': address,
                    'mnemonic': mnemonic}
        except Exception as er:
            gui_errorDialog.Error('fromMnemonic', str(er)).exec()
            return {}
