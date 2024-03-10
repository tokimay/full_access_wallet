from binascii import a2b_hex
from hashlib import sha256, pbkdf2_hmac
from src import gui_errorDialog, qui_getUserInput
from src.dataTypes import TYPE
from src.validators import checkType, checkLen


def entropyToSha256(entropy: str) -> str:
    try:
        if not checkType('entropyToSha256', entropy, TYPE.STRING):
            return ''
        if entropy.startswith('0b'):
            entropy = entropy[2:]
        if not checkLen('entropyToSha256', entropy, 256):
            return ''
        else:
            hexString = "{0:0>4X}".format(int(entropy, 2))
            data = a2b_hex(hexString)
            hashEntropy = sha256(data).hexdigest()
            return bin(int(str(hashEntropy), 16))[2:].zfill(256)  # should check zfill
    except Exception as er:
        gui_errorDialog.Error('entropyToSha256', str(er)).exec()
        return ''


def entropyToPbkdf2HmacSha256(entropy: str) -> str:
    try:
        if not checkType('entropyToPbkdf2HmacSha256', entropy, TYPE.STRING):
            return ''
        if entropy.startswith('0b'):
            entropy = entropy[2:]
        if not checkLen('entropyToPbkdf2HmacSha256', entropy, 256):
            return ''
        else:
            getPassphrase = qui_getUserInput.Ui('Passphrase for wallet',
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
        gui_errorDialog.Error('entropyToPbkdf2HmacSha256', str(er)).exec()
        return ''
