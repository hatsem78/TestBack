import hashlib

from Cryptodome.Cipher import AES as domeAES
from Cryptodome.Random import get_random_bytes
from Crypto import Random
from Crypto.Cipher import AES as cryptoAES
import base64
SECRET_KEY = ''


class Crypt:

    __BLOCK_SIZE = domeAES.block_size
    __key = '12#$%&"!°1456321=)(kjlJNMVaqwe'
    __key = (__key + SECRET_KEY).encode()
    __key__ = hashlib.sha256(__key).digest()

    def __pad(self, raw):
        block_size = cryptoAES.block_size
        pad = raw + (block_size - len(raw) % block_size) * chr(block_size - len(raw) % block_size)
        return pad

    def encrypt(self, raw):
        raw = base64.b64encode(self.__pad(raw).encode('utf8'))
        random_bytes = get_random_bytes(cryptoAES.block_size)
        cipher = cryptoAES.new(key=self.__key__, mode=cryptoAES.MODE_CFB, iv=random_bytes)
        encode64 = base64.b64encode(random_bytes + cipher.encrypt(raw))
        new_random = Random.new().read(self.__BLOCK_SIZE)
        aes = domeAES.new(self.__key__, domeAES.MODE_CFB, new_random)
        crypt = base64.b64encode(new_random + aes.encrypt(encode64))
        return crypt.decode('utf-8')

    def __unpad(self, raw):
        unpad = raw[:-ord(raw[-1:])]
        return unpad

    def decrypt(self, enc):

        passphrase = self.__key__
        encrypted = base64.b64decode(enc)
        encrypt_block = encrypted[:self.__BLOCK_SIZE]
        aes = domeAES.new(passphrase, domeAES.MODE_CFB, encrypt_block)
        enc = aes.decrypt(encrypted[self.__BLOCK_SIZE:])
        enc = base64.b64decode(enc)
        iv = enc[:cryptoAES.block_size]
        cipher = cryptoAES.new(self.__key__, cryptoAES.MODE_CFB, iv)
        block = self.__unpad(base64.b64decode(cipher.decrypt(enc[cryptoAES.block_size:])))
        return block
