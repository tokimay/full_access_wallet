import binascii
import hashlib
from hashlib import sha256

from src import gui_errorDialog, qui_getUserChoice, gui_mouseTracker, database, qui_getUserInput
from src.ellipticCurve import secp256k1
from sha3 import keccak_256

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
            gui_errorDialog.Error(str(er)).exec()
            return ''

    @staticmethod
    def entropyToPrivateKey(entropy: str) -> str:
        try:
            if not isinstance(entropy, str):
                (gui_errorDialog.Error('Entropy received by type ' + str(type(entropy)) +
                                       '.\nexpected binary string.').exec())
                return ''
            if entropy.startswith('0b'):
                entropy = entropy[2:]
            if not len(entropy) == 256:
                gui_errorDialog.Error(
                    'Entropy by len ' + str(len(entropy)) + ' bit received.\nexpected 256 bit.').exec()
                return ''
            else:
                pbkdf2HmacSha512PrivateKey = New.entropyToPbkdf2HmacSha512(entropy)

                return pbkdf2HmacSha512PrivateKey  # need complete by hashing
        except Exception as er:
            gui_errorDialog.Error(str(er)).exec()
            return ''

    @staticmethod
    def privateKeyToPublicKeyCoordinate(privateKey: str) -> tuple:
        try:
            if not isinstance(privateKey, str):
                (gui_errorDialog.Error('PrivateKey received by type ' + str(type(privateKey)) +
                                       '.\nexpected hex string.').exec())
                return ()
            if privateKey.startswith('0x') or privateKey.startswith('0X'):
                privateKey = privateKey[2:]
            if not New.checkHex(privateKey):
                gui_errorDialog.Error('PrivateKey key receives in none hex format.').exec()
                return ()
            elif len(privateKey) == 64 or len(privateKey) == 128:
                curve = secp256k1()
                publicKeyCoordinate = curve.getPublicKeyCoordinate(int(privateKey, 16))
                if len(publicKeyCoordinate) <= 0:
                    gui_errorDialog.Error('Getting coordinate from elliptic curve failed.').exec()
                    return ()
                else:
                    return publicKeyCoordinate
            else:
                gui_errorDialog.Error(
                    'PrivateKey by len ' + str(len(privateKey)) + ' received.\nexpected 64 or 128.').exec()
                return ()
        except Exception as er:
            gui_errorDialog.Error(str(er)).exec()
            return ()

    @staticmethod
    def publicKeyCoordinateToPublicKey(coordinate: tuple) -> str:
        try:
            if not isinstance(coordinate, tuple):
                (gui_errorDialog.Error('PrivateKey received by type ' + str(type(coordinate)) +
                                       '.\nexpected tuple.').exec())
                return ''
            elif len(coordinate) == 0:
                gui_errorDialog.Error('Coordinate with length 0 is not calculable.').exec()
                return ''
            else:
                coordinate_x_y = (coordinate[0].to_bytes(32, byteorder='big') +
                                  coordinate[1].to_bytes(32, byteorder='big'))
                return '0x' + coordinate_x_y.hex()
        except Exception as er:
            gui_errorDialog.Error(str(er)).exec()
            return ''

    @staticmethod
    def publicKeyToAddress(publicKey: str) -> str:
        try:
            if not isinstance(publicKey, str):
                (gui_errorDialog.Error('PublicKey received by type ' + str(type(publicKey)) +
                                       '.\nexpected hex string.').exec())
                return ''
            if publicKey.startswith('0x') or publicKey.startswith('0X'):
                publicKey = publicKey[2:]
            if not New.checkHex(publicKey):
                gui_errorDialog.Error('Public key receives in none hex format.').exec()
                return ''
            elif not len(publicKey) == 128:
                gui_errorDialog.Error(
                    'PublicKey by len ' + str(len(publicKey)) + ' received.\nexpected 128.').exec()
                return ''
            else:
                return '0x' + keccak_256(bytes.fromhex(publicKey)).digest()[-20:].hex()
        except Exception as er:
            gui_errorDialog.Error(str(er)).exec()
            return ''

    @staticmethod
    def entropyToMnemonic(entropy: str) -> str:
        try:
            if not isinstance(entropy, str):
                (gui_errorDialog.Error('Entropy received by type ' + str(type(entropy)) +
                                       '.\nexpected binary string.').exec())
                return ''
            if entropy.startswith('0b'):
                entropy = entropy[2:]
            if not len(entropy) == 256:
                gui_errorDialog.Error(
                    'Entropy by len ' + str(len(entropy)) + ' bit received.\nexpected 256 bit.').exec()
                return ''
            else:
                bip39 = []
                mnemonic = []
                with open('resources/bip39EnglishWordList.txt') as file:
                    while line := file.readline():
                        bip39.append(line.strip())
                    sha256Entropy = New.entropyToSha256(entropy)
                    if sha256Entropy.startswith('0b'):
                        sha256Entropy = entropy[2:]
                    if not len(sha256Entropy) == 256:
                        gui_errorDialog.Error('Hashed entropy by len ' + str(len(sha256Entropy))
                                              + ' bit received.\nexpected 256 bit.').exec()
                        return ''
                    else:
                        checkSumEntropy = entropy + str(sha256Entropy[:8])
                        if not len(checkSumEntropy) == 264:
                            gui_errorDialog.Error('CheckSum entropy by len ' + str(len(sha256Entropy))
                                                  + ' bit received.\nexpected 264 bit').exec()
                            return ''
                        else:
                            chunk = 11
                            while chunk <= 264:
                                mnemonic.append(bip39[int(checkSumEntropy[(chunk - 11):chunk], 2)])
                                chunk = chunk + 11
                            if not len(mnemonic) == 24:
                                gui_errorDialog.Error('Generating mnemonic failed. \nIncompatible length received.\n' +
                                                      str(len(mnemonic))).exec()
                                return ''
                            else:
                                return ' '.join(mnemonic)
        except Exception as er:
            gui_errorDialog.Error(str(er)).exec()
            return ''

    @staticmethod
    def checkHex(hexNumber):
        try:
            int(hexNumber, 16)
            return True
        except ValueError:
            return False

    @staticmethod
    def entropyToSha256(entropy: str) -> str:
        try:
            if not isinstance(entropy, str):
                (gui_errorDialog.Error('Entropy received by type ' + str(type(entropy)) +
                                       '.\nexpected binary string.').exec())
                return ''
            if entropy.startswith('0b'):
                entropy = entropy[2:]
            if not len(entropy) == 256:
                gui_errorDialog.Error(
                    'Entropy by len ' + str(len(entropy)) + ' bit received.\nexpected 256 bit.').exec()
                return ''
            else:
                hexString = "{0:0>4X}".format(int(entropy, 2))
                data = binascii.a2b_hex(hexString)
                hashEntropy = sha256(data).hexdigest()
                return bin(int(str(hashEntropy), 16))[2:].zfill(256)  # should check zfill ???????????????????
        except Exception as er:
            gui_errorDialog.Error(str(er)).exec()
            return ''

    @staticmethod
    def entropyToPbkdf2HmacSha512(entropy: str) -> str:
        try:
            if not isinstance(entropy, str):
                (gui_errorDialog.Error('Entropy received by type ' + str(type(entropy)) +
                                       '.\nexpected binary string.').exec())
                return ''
            if entropy.startswith('0b'):
                entropy = entropy[2:]
            if not len(entropy) == 256:
                gui_errorDialog.Error(
                    'Entropy by len ' + str(len(entropy)) + ' bit received.\nexpected 256 bit.').exec()
                return ''
            else:
                getPassphrase = qui_getUserInput.Ui('Passphrase for wallet',
                                                    'Enter passphrase for wallet:\n'
                                                    'cancel to skip')
                getPassphrase.exec()
                passphrase = getPassphrase.getInput()
                if passphrase == '':  # canceled by user
                    pbkdf2Entropy = hashlib.pbkdf2_hmac('sha256', str.encode('mnemonic'),
                                                        str.encode(entropy), 2048)
                else:
                    pbkdf2Entropy = hashlib.pbkdf2_hmac('sha512', str.encode(passphrase),
                                                        str.encode(entropy), 2048)
                return pbkdf2Entropy.hex()
        except Exception as er:
            gui_errorDialog.Error(str(er)).exec()
            return ''

    @staticmethod
    def mnemonicToEntropy(mnemonic: str) -> str:
        try:
            bip39 = []
            entropy = ''
            with open('resources/bip39EnglishWordList.txt') as file:
                while line := file.readline():
                    bip39.append(line.strip())
            mnemonicList = mnemonic.split()
            if not len(mnemonicList) == 24:
                gui_errorDialog.Error(
                    'Mnemonic by len ' + str(len(mnemonicList)) + ' words received.\nexpected 24 words.').exec()
                return ''
            else:
                for word in mnemonicList:
                    if not (word in bip39):
                        gui_errorDialog.Error('Invalid Mnemonic.\n' + str(word) + ' is not in BIP39 word list').exec()
                        return ''
                    else:
                        index = bin(bip39.index(word))[2:].zfill(11)
                        entropy = entropy + index
                if not len(entropy) == 264:
                    gui_errorDialog.Error(
                        'recovered check summed entropy by ' + str(len(entropy)) +
                        ' bit length generated .\nexpected 264 bit.').exec()
                    return ''
                else:
                    checkSum = entropy[-8:]
                    entropy = entropy[:-8]  # remove checksum
                    sha256Entropy = New.entropyToSha256(entropy)
                    if sha256Entropy.startswith('0b'):
                        sha256Entropy = entropy[2:]
                    if not len(sha256Entropy) == 256:
                        gui_errorDialog.Error('Calculation failed.').exec()
                        return ''
                    if not checkSum == str(sha256Entropy[:8]):
                        gui_errorDialog.Error('Invalid Mnemonic.').exec()
                        return ''
                    else:
                        return entropy
        except Exception as er:
            gui_errorDialog.Error(str(er)).exec()
            return ''

    @staticmethod
    def random() -> dict:
        try:
            entropy = New.newEntropy()
            if entropy == '':
                return {}
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
            gui_errorDialog.Error(str(er)).exec()
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
            gui_errorDialog.Error(str(er)).exec()
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
            gui_errorDialog.Error(str(er)).exec()
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
            gui_errorDialog.Error(str(er)).exec()
            return {}
