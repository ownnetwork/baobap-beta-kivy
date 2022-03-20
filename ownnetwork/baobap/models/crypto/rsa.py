# MIT License -> LISCENCE.mit

from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
import json

"""
RSA Encryptation
"""
class RSA_E(object):

    def __init__(self):
        pass

    def encrypt(self, public_key, data):
        cipher = PKCS1_OAEP.new(RSA.import_key(public_key))
        return cipher.encrypt(data)

    def decrypt(self, private_key, data):
        cipher = PKCS1_OAEP.new(RSA.import_key(private_key))
        return cipher.decrypt(data)
