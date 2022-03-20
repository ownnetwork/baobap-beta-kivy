# MIT License -> LISCENCE.mit

from ownnetwork.baobap.models.crypto.rsa import RSA_E

from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
import json

"""
Encrypt data with public key and crypto type
"""
class UNIVERSALCrypto(object):
    """docstring for ."""

    def __init__(self):
        pass

    def encrypt_data(self, public_key, data, type_encryptation = 'RSA'):
        if type_encryptation == "RSA":
            return RSA_E().encrypt(public_key, data)

    def decrypt_data(self, private_key, data,  type_encryptation = 'RSA'):
        if type_encryptation == "RSA":
            return RSA_E().decrypt(private_key, data)
