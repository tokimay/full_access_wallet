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
    def __init__(self):  # an00
        pass

    @staticmethod
    def random() -> dict:  # anf01
        mouseTracker = gui_mouseTracker.UI()
        mouseTracker.exec()
        entropy = mouseTracker.getEntropy()
        if not len(entropy) == 256:
            gui_errorDialog.Error('Entropy by len ' + str(len(entropy)) + ' bit received.\nexpected 256 bit.\n'
                                                                          'error code: anf01.1').exec()
            return {}
        else:
            acc = New.fromEntropy(int(entropy, 2))
            acc['entropy'] = entropy
            return acc
        """
        if not isinstance(acc, dict) or len(acc) == 0:
            gui_errorDialog.Error('Account creation failed \n ' + str(type(acc))).exec()
            acc = {}
        else:
            acc['entropy'] = entropy  # append entropy to dict
        return acc
        """

    @staticmethod
    def generateMnemonic(entropy: str) -> str:  # anf02
        bip39 = []
        mnemonic = []
        with open('resources/bip39EnglishWordList.txt') as file:
            while line := file.readline():
                bip39.append(line.strip())
        if not len(entropy) == 256:
            gui_errorDialog.Error('Entropy by len ' + str(len(entropy)) + ' bit received.\nexpected 256 bit.\n'
                                                                          'error code: anf02.1').exec()
            return ''
        else:
            sha256Entropy = New.entropyToSha256(entropy)
            if not len(sha256Entropy) == 256:
                gui_errorDialog.Error('Hashed entropy by len ' + str(len(sha256Entropy))
                                      + ' bit received.\nexpected 256 bit.\n'
                                        'error code: anf02.2').exec()
                return ''
            else:
                checkSumEntropy = entropy + str(sha256Entropy[:8])
                if not len(checkSumEntropy) == 264:
                    gui_errorDialog.Error('CheckSum entropy by len ' + str(len(sha256Entropy))
                                          + ' bit received.\nexpected 264 bit.\nerror code: anf02.3').exec()
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

    @staticmethod
    def fromEntropy(entropy: int) -> dict:  # anf03
        if not isinstance(entropy, int):
            gui_errorDialog.Error('Entropy received by type ' + str(type(entropy)) + '.\nexpected integer.\n'
                                                                                     'error code: anf03.1').exec()
            return {}
        else:
            privateKey = hex(entropy)
            return New.fromPrivateKey(privateKey)

    @staticmethod
    def entropyToSha256(entropy):  # anf04
        if not isinstance(entropy, str):
            gui_errorDialog.Error('Entropy received by type ' + str(type(entropy)) + '.\nexpected string.\n'
                                                                                     'error code: anf04.1').exec()
            return {}
        elif not len(entropy) == 256:
            gui_errorDialog.Error('Entropy by len ' + str(len(entropy)) + ' bit received.\nexpected 256 bit.\n'
                                                                          'error code: anf04.2').exec()
            return {}
        else:
            hexString = "{0:0>4X}".format(int(entropy, 2))
            data = binascii.a2b_hex(hexString)
            hashEntropy = sha256(data).hexdigest()
            res = bin(int(str(hashEntropy), 16))[2:].zfill(256)  # should check zfill ???????????????????
            return res

    @staticmethod
    def fromPrivateKey(privateKey):  # anf05
        if not New.checkHex(privateKey):
            gui_errorDialog.Error('Private key receives in none hex format.\nerror code: anf05.1').exec()
            return {}
        else:
            curve = secp256k1()
            publicKeyCoordinate = curve.getPublicKeyCoordinate(int(privateKey, 16))
            if len(publicKeyCoordinate) <= 0:
                gui_errorDialog.Error('Getting coordinate from elliptic curve failed.\nerror code: anf05.2').exec()
                return {}
            else:
                coordinate_x_y = (publicKeyCoordinate[0].to_bytes(32, byteorder='big') +
                                  publicKeyCoordinate[1].to_bytes(32, byteorder='big'))
                publicKey = '0x' + coordinate_x_y.hex(), type(coordinate_x_y.hex())
                address = '0x' + keccak_256(coordinate_x_y).digest()[-20:].hex()
                return {'privateKey': privateKey, 'publicKeyCoordinate': publicKeyCoordinate,
                        'publicKey': publicKey[0], 'address': address}

    """
        # print('private_key: 0x' + private_key.hex())

        public_key = PublicKey.from_valid_secret(private_key).format(compressed=False)[1:]
        # print('public_key : 0x' + public_key.hex())

        address = keccak_256(public_key).digest()[-20:]
        # print('address    : 0x' + address.hex())
        return '0x' + public_key.hex(), '0x' + address.hex()
        """

    @staticmethod
    def checkHex(hexNumber):
        try:
            int(hexNumber, 16)
            return True
        except ValueError:
            return False


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
