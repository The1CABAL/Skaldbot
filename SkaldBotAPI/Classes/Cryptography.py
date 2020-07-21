from Classes.ConfigParser import *
from cryptography.fernet import Fernet

class Cryptography():
    def getkey():
        values = LoadConfig('config.ini', 'cryptography')

        key = values['cryptography.key']
        key = str(key)
        key = key.encode()
        return key

    def hashPassword(password):
        key = Cryptography.getkey()
        cipher_suite = Fernet(key)
        ciphered_text = cipher_suite.encrypt(password.encode())

        return ciphered_text;

    def dehashPassword(password):
        key = Cryptography.getkey()
        cipher_suite = Fernet(key)
        uncipher_text = cipher_suite.decrypt(password.encode())
        plain_text = bytes(uncipher_text).decode("utf-8")

        return plain_text
