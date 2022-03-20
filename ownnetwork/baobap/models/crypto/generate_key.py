# MIT License -> LISCENCE.mit

from Crypto.PublicKey import RSA


"""
Generate encrypted key
"""
class GenerateKey():
    def __init__(self, typekey: str, keysize: int):

        self.typekey, self.keysize = typekey, keysize

        if typekey == "RSA":
            self.RSA_key()

    def RSA_key(self):
        private_key = RSA.generate(self.keysize)
        self.private_key = private_key.exportKey("PEM").decode()
        self.public_key = private_key.publickey().export_key("PEM").decode()
