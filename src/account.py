import binascii
from hashlib import sha256

from src import gui_errorDialog, qui_create_newAccount
from src.gui_mouseTracker import MouseTracker
from src.secp256k1 import getPublicKeyCoortinate
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


def generateEntropy():
    mouseTrackerWindow = MouseTracker()
    mouseTrackerWindow.exec()
    return mouseTrackerWindow.getEntropy()


def createAccount(db, message):
    createAccount_window = qui_create_newAccount.Ui(message)  # "Some account already exist")
    createAccount_window.exec()
    entropy = createAccount_window.getEntropy()
    mnemonic = generateMnemonic(entropy)
    print(mnemonic)
    print(type(mnemonic))
    acc = None
    address = 'None'
    if isinstance(entropy, str) and len(entropy) == 256 and entropy != 'init':
        acc = fromEntropy(entropy)
        if isinstance(acc, dict):
            print('privateKeyHex', hex(acc['privateKey']), type(acc['privateKey']))
            print('publicKeyCoordinate', acc['publicKeyCoordinate'], type(acc['publicKeyCoordinate']))
            print('publicKey', hex(acc['publicKey']), type(acc['publicKey']))
            print('address', hex(acc['address']), type(acc['address']))
            db.insertRow(acc)
            address = hex(acc['address'])
        else:
            err = gui_errorDialog.Error('Account creation failed \n ' + str(type(acc)))
            err.exec()
    else:
        if entropy == 'init':
            pass
        elif not isinstance(entropy, str):
            err = gui_errorDialog.Error('Entropy received by type ' + str(type(entropy)) + '.\nexpected string')
            err.exec()
        else:
            err = gui_errorDialog.Error('Entropy by len ' + str(len(entropy)) + ' bit received.\nexpected 256 bit')
            err.exec()
    return address
    # return fromEntropy(generateEntropy())


def fromEntropy(entropy: str) -> dict:
    privateKey = hex(int(entropy, 2))
    publicKeyCoordinate = getPublicKeyCoortinate(int(entropy, 2))
    coordinate_x_y = (publicKeyCoordinate[0].to_bytes(32, byteorder='big') +
                      publicKeyCoordinate[1].to_bytes(32, byteorder='big'))
    publicKey = '0x' + coordinate_x_y.hex(), type(coordinate_x_y.hex())
    address = '0x' + keccak_256(coordinate_x_y).digest()[-20:].hex()
    return {'privateKey': int(privateKey, 0), 'publicKeyCoordinate': publicKeyCoordinate,
            'publicKey': int(publicKey[0], 0), 'address': int(address, 0)}


def entropyToSha256(entropy):
    if len(entropy) == 256:
        print(entropy)  # ============================================================================
        hexString = "{0:0>4X}".format(int(entropy, 2))
        data = binascii.a2b_hex(hexString)
        hashEntropy = sha256(data).hexdigest()
        return bin(int(str(hashEntropy), 16))[2:]
    else:
        err = gui_errorDialog.Error('Entropy by len ' + str(len(entropy)) + ' bit received.\nexpected 256 bit.\n'
                                                                            'hashing entropy failed failed.')
        err.exec()


def generateMnemonic(entropy):
    bip39 = []
    mnemonic = []
    with open('resources/bip39EnglishWordList.txt') as file:
        while line := file.readline():
            bip39.append(line.strip())

    sha256Entropy = entropyToSha256(entropy)
    #if len(sha256Entropy) == 256:
    print('check sum .zfill(256)= ', sha256Entropy.zfill(256)[:8])
    print('check sum = ', sha256Entropy[:8])
    checkSumEntropy = entropy + sha256Entropy.zfill(256)[:8]
    if len(checkSumEntropy) == 264:
        chunk = 11
        while chunk <= 264:
            mnemonic.append(bip39[int(checkSumEntropy[(chunk - 11):chunk], 2)])
            chunk = chunk + 11
        if len(mnemonic) == 24:
            return ' '.join(mnemonic)
        else:
            err = gui_errorDialog.Error('Generating mnemonic failed. \nIncompatible length received.\n'+
                                        str(len(mnemonic)))
            err.exec()
            return None
        #else:
        #    err = gui_errorDialog.Error('CheckSum entropy by len ' + str(len(sha256Entropy))
        #                                + ' bit received.\nexpected 264 bit')
        #    err.exec()
        #    return None
    else:
        err = gui_errorDialog.Error('Hashed entropy by len ' + str(len(sha256Entropy))
                                    + ' bit received.\nexpected 256 bit')
        err.exec()
        return None


def fromMnemonic(memo):
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
