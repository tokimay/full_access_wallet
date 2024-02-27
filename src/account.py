import binascii
from hashlib import sha256

from src import gui_errorDialog, qui_getUserChoice, gui_mouseTracker, database
from src.ellipticCurve import secp256k1
from sha3 import keccak_256

"""
ETHEREUM_DEFAULT_PATH = "m/44'/60'/0'/0/0"
def seed_from_mnemonic(words: str, passphrase: str) -> bytes:
    lang = Mnemonic.detect_language(words)
    expanded_words = Mnemonic(lang).expand(words)
    if not Mnemonic(lang).is_mnemonic_valid(expanded_words):
        raise ValidationError(
            f"Provided words: '{expanded_words}', are not a "
            "valid BIP39 mnemonic phrase!"
        )
    return Mnemonic.to_seed(expanded_words, passphrase)

"""


class New:
    def __init__(self):
        pass

    @staticmethod
    def random() -> dict:
        acc = {}
        mouseTracker = gui_mouseTracker.UI()
        mouseTracker.exec()
        entropy = mouseTracker.getEntropy()
        if not isinstance(entropy, str):
            err = gui_errorDialog.Error('Entropy received by type ' + str(type(entropy)) + '.\nexpected string')
            err.exec()
        elif not len(entropy) == 256:
            err = gui_errorDialog.Error('Entropy by len ' + str(len(entropy)) + ' bit received.\nexpected 256 bit')
            err.exec()
        else:
            acc = New.fromEntropy(entropy)
            if not isinstance(acc, dict) or len(acc) == 0:
                err = gui_errorDialog.Error('Account creation failed \n ' + str(type(acc)))
                err.exec()
                acc = {}
            else:
                acc['entropy'] = entropy  # append entropy to dict
        return acc

    @staticmethod
    def generateMnemonic(entropy: str) -> str:
        bip39 = []
        mnemonic = []
        with open('resources/bip39EnglishWordList.txt') as file:
            while line := file.readline():
                bip39.append(line.strip())
        if not len(entropy) == 256:
            err = gui_errorDialog.Error('Entropy by len ' + str(len(entropy)) + ' bit received.\nexpected 256 bit')
            err.exec()
            return ''
        else:
            sha256Entropy = New.entropyToSha256(entropy)
            checkSumEntropy = entropy + sha256Entropy.zfill(256)[:8]
            if not len(sha256Entropy) == 256:
                err = gui_errorDialog.Error('Hashed entropy by len ' + str(len(sha256Entropy))
                                            + ' bit received.\nexpected 256 bit')
                err.exec()
                return ''
            else:
                if not len(checkSumEntropy) == 264:
                    err = gui_errorDialog.Error('CheckSum entropy by len ' + str(len(sha256Entropy))
                                                + ' bit received.\nexpected 264 bit')
                    err.exec()
                    return ''
                else:
                    chunk = 11
                    while chunk <= 264:
                        mnemonic.append(bip39[int(checkSumEntropy[(chunk - 11):chunk], 2)])
                        chunk = chunk + 11
                    if not len(mnemonic) == 24:
                        err = gui_errorDialog.Error('Generating mnemonic failed. \nIncompatible length received.\n' +
                                                    str(len(mnemonic)))
                        err.exec()
                        return ''
                    else:
                        return ' '.join(mnemonic)

    @staticmethod
    def fromEntropy(entropy: str) -> dict:
        privateKey = hex(int(entropy, 2))
        curve = secp256k1()
        publicKeyCoordinate = curve.getPublicKeyCoordinate(int(entropy, 2))
        if len(publicKeyCoordinate) <= 0:
            err = gui_errorDialog.Error('Getting coordinate from elliptic curve failed')
            err.exec()
            return {}
        else:
            coordinate_x_y = (publicKeyCoordinate[0].to_bytes(32, byteorder='big') +
                              publicKeyCoordinate[1].to_bytes(32, byteorder='big'))
            publicKey = '0x' + coordinate_x_y.hex(), type(coordinate_x_y.hex())
            address = '0x' + keccak_256(coordinate_x_y).digest()[-20:].hex()
            return {'privateKey': privateKey, 'publicKeyCoordinate': publicKeyCoordinate,
                    'publicKey': publicKey[0], 'address': address}

    @staticmethod
    def entropyToSha256(entropy):
        if len(entropy) == 256:
            print(len(entropy))
            print('====================')
            hexString = "{0:0>4X}".format(int(entropy, 2))
            print(hexString)
            print(len(hexString))
            print('====================')
            data = binascii.a2b_hex(hexString)
            print(data)
            print(len(data))
            print('====================')
            hashEntropy = sha256(data).hexdigest()
            print(hashEntropy)
            print(len(hashEntropy))
            print('====================')
            res = bin(int(str(hashEntropy), 16))[2:].zfill(256)  # should check zfill ???????????????????
            print(res)
            print(len(res))
            print('====================')
            return res
        else:
            err = gui_errorDialog.Error('Entropy by len ' + str(len(entropy)) + ' bit received.\nexpected 256 bit.\n'
                                                                                'hashing entropy failed failed.')
            err.exec()


def fromMnemonic(memo):
    bip39 = []
    with open('resources/bip39EnglishWordList.txt') as file:
        while line := file.readline():
            bip39.append(line.strip())
    mnemonicList = memo.split()

    print(mnemonicList)

    pass
    """
        # The use of the Mnemonic features of Account is disabled by default
        Account.enable_unaudited_hdwallet_features()
        acct = Account.from_mnemonic(memo)

        private_key_bytes = decode_hex(acct.key.hex())
        private_key = keys.PrivateKey(private_key_bytes)
        # print('private_key:', private_key)

        public_key = private_key.public_key
        # print('public_key :', public_key)

        # print('address    :', acct.address)
        return private_key, public_key, acct.address
    """


def fromPrivateKey(private_key):
    pass
    """
        # print('private_key: 0x' + private_key.hex())

        public_key = PublicKey.from_valid_secret(private_key).format(compressed=False)[1:]
        # print('public_key : 0x' + public_key.hex())

        address = keccak_256(public_key).digest()[-20:]
        # print('address    : 0x' + address.hex())
        return '0x' + public_key.hex(), '0x' + address.hex()
        """
