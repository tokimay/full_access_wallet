from src.gui_mouseTracker import MouseTracker
from src.secp256k1 import getPublicKeyCoortinate
from sha3 import keccak_256


def generateEntropy():
    mouseTrackerWindow = MouseTracker()
    mouseTrackerWindow.exec()
    return mouseTrackerWindow.getEntropy()


def createAccount():
    return fromEntropy(generateEntropy())


def fromEntropy(entropy: str) -> dict:
    privateKey = hex(int(entropy, 2))
    publicKeyCoordinate = getPublicKeyCoortinate(int(entropy, 2))
    coordinate_x_y = (publicKeyCoordinate[0].to_bytes(32, byteorder='big') +
                      publicKeyCoordinate[1].to_bytes(32, byteorder='big'))
    publicKey = '0x' + coordinate_x_y.hex(), type(coordinate_x_y.hex())
    address = '0x' + keccak_256(coordinate_x_y).digest()[-20:].hex()
    return {'privateKey': int(privateKey, 0), 'publicKeyCoordinate': publicKeyCoordinate,
            'publicKey': int(publicKey[0], 0), 'address': int(address, 0)}


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
