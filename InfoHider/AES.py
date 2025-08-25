import logging
import base64
import binascii
from Crypto.Cipher import AES

class AESCrypt:
    """
    AES/CBC/PKCS5Padding 加密
    """
    def __init__(self, key):
        if len(key) != 16:
            raise RuntimeError('密钥长度非16位!!!')

        self.key = str.encode(key)
        self.iv = bytes(16)
        self.MODE = AES.MODE_CBC
        self.block_size = 16
        # 填充函数
        self.padding = lambda data: data + (self.block_size - len(data.encode('utf-8')) % self.block_size) * chr(
            self.block_size - len(data.encode('utf-8')) % self.block_size)
        # 截断函数
        self.unpadding = lambda data: data[:-ord(data[-1])]


    def aes_encrypt(self, plaintext):
        try:
            padding_text = self.padding(plaintext).encode("utf-8")
            cryptor = AES.new(self.key, self.MODE, self.iv)
            encrypt_aes = cryptor.encrypt(padding_text)
            encrypt_text = (base64.b64encode(encrypt_aes)).decode()
            return encrypt_text
        except Exception as e:
            logging.exception(e)


    def aes_decrypt(self, ciphertext):
        try:
            cryptor = AES.new(self.key, self.MODE, self.iv)
            plain_base64 = base64.b64decode(ciphertext)
            decrypt_text = cryptor.decrypt(plain_base64)
            plain_text = self.unpadding(decrypt_text.decode("utf-8"))
            return plain_text
        except UnicodeDecodeError as e:
            logging.error('解密失败,请检查密钥是否正确!')
            logging.exception(e)
        except binascii.Error as e:
            logging.exception(e)
        except Exception as e:
            logging.exception(e)


