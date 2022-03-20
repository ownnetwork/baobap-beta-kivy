# MIT License -> LISCENCE.mit

from ownnetwork.baobap.models.crypto.generate_key import GenerateKey
from os import path
import json

"""
Add a account to the json acccount file
"""
class AddAccount(object):

    def __init__(self, account_id: str, password: str, hostinfo: dict, type_encryptation = 'RSA', keysize = 2048):

        # prevent a interfering file with the creation of a folder
        account_id = account_id.replace('/','')

        if path.exists('db/accounts.json'):
            with open("db/accounts.json", 'r+') as f:
                jsondata = json.load(f)
                if not jsondata.get(account_id):
                    key_generate = GenerateKey(type_encryptation, 2048)

                    account_data = {
                        account_id: {
                            "host": hostinfo['host'],
                            "port": hostinfo['port'],
                            "password": password,
                            "private_key": key_generate.private_key,
                            "public_key": key_generate.public_key,
                            "type_crypto": type_encryptation,
                            "key_size": keysize,
                            }
                        }

                    jsondata.update(account_data)
                    f.seek(0)
                    json.dump(jsondata, f, indent=2)
