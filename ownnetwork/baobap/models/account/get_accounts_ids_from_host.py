# MIT License -> LISCENCE.mit

import json

"""
Get account(s) list id from host and port
"""
def GetAccountsIdsFromHost(host: str, port: int):
    account_list = []

    with open("db/accounts.json", 'r') as f:
        for key, value in json.load(f).items():
            if value["host"] == host and value["port"] == port:
                account_list.append(key)

    return account_list