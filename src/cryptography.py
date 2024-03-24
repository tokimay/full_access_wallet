from binascii import a2b_hex
from hashlib import sha256, pbkdf2_hmac
from base64 import b64encode, b64decode
from Crypto.Cipher import AES as AESalgo
from Crypto.Hash import SHA256
from Crypto import Random
from src.GUI import gui_userInput
from src.dataTypes import TYPE
from src.validators import checkType, checkLen


class ENTROPY:
    def __init__(self):
        pass

    @staticmethod
    def ToSha256(entropy: str) -> str:
        try:
            checkType(entropy, TYPE.STRING)
            if entropy.startswith('0b'):
                entropy = entropy[2:]
            checkLen(entropy, 256)

            hexString = "{0:0>4X}".format(int(entropy, 2))
            data = a2b_hex(hexString)
            hashEntropy = sha256(data).hexdigest()
            return bin(int(str(hashEntropy), 16))[2:].zfill(256)  # should check zfill
        except Exception as er:
            raise Exception(f"ToSha256 -> {er}")

    @staticmethod
    def ToPbkdf2HmacSha256(entropy: str) -> str:
        try:
            checkType(entropy, TYPE.STRING)
            if entropy.startswith('0b'):
                entropy = entropy[2:]
            checkLen(entropy, 256)
            getPassphrase = gui_userInput.WINDOW('Passphrase for wallet',
                                                 'Enter passphrase for wallet:\n'
                                                 'cancel to skip')
            getPassphrase.exec()
            passphrase = getPassphrase.getInput()
            if passphrase == '':  # canceled by user
                # pbkdf2Entropy = hashlib.pbkdf2_hmac('sha512', str.encode('mnemonic'),
                #                                    str.encode(entropy), 2048)
                pbkdf2Entropy = pbkdf2_hmac('sha256', str.encode('mnemonic'),
                                            str.encode(entropy), 2048)
            else:
                # pbkdf2Entropy = hashlib.pbkdf2_hmac('sha512', str.encode(passphrase),
                #                                    str.encode(entropy), 2048)
                pbkdf2Entropy = pbkdf2_hmac('sha256', str.encode(passphrase),
                                            str.encode(entropy), 2048)
            return pbkdf2Entropy.hex()
        except Exception as er:
            raise Exception(f"ToPbkdf2HmacSha256 -> {er}")


class AES:
    def __init__(self):
        pass

    @staticmethod
    def encrypt(key, source, encode=True):
        try:
            key = SHA256.new(key).digest()
            IV = Random.new().read(AESalgo.block_size)  # generate IV
            encryptor = AESalgo.new(key, AESalgo.MODE_CBC, IV)
            padding = AESalgo.block_size - len(source) % AESalgo.block_size
            source += bytes([padding]) * padding
            data = IV + encryptor.encrypt(source)
            return b64encode(data).decode("utf-8") if encode else data  # latin-1
        except Exception as er:
            raise Exception(f"encrypt -> {er}")

    @staticmethod
    def decrypt(key, source, decode=True):
        try:
            if decode:
                source = b64decode(source.encode("utf-8"))  # latin-1
            key = SHA256.new(key).digest()
            IV = source[:AESalgo.block_size]  # extract the IV from the beginning
            decryptor = AESalgo.new(key, AESalgo.MODE_CBC, IV)
            data = decryptor.decrypt(source[AESalgo.block_size:])
            padding = data[-1]  # pick the padding value from the end
            if data[-padding:] != bytes([padding]) * padding:
                raise ValueError("Invalid padding...")
            return data[:-padding]  # remove the padding
        except Exception as er:
            raise Exception(f"decrypt -> {er}")
