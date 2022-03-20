import json
from base64 import b64decode, b64encode

from ownnetwork.baobap.models.contact.add_contact import AddContact
from ownnetwork.baobap.models.account.add_account import AddAccount
from ownnetwork.baobap.models.account.get_accounts_ids_from_host import GetAccountsIdsFromHost
from ownnetwork.baobap.api import NodeHostAPI
from ownnetwork.utils import password_gen

class DataActions(object):

    def _adding_account(self):
        server = NodeHostAPI(self.host, self.port, False)
        password = password_gen(60)
        account_id = server.create_new_account(password)
        
        hostinfo_json = {'host': self.host, 'port': self.port}
        AddAccount(account_id, password, hostinfo_json)
        
        return account_id

    def adding_contact(self, jsondata: list):

        self.jsondata = jsondata
        if jsondata.get("host") and jsondata.get("port"):
            self.host, self.port = jsondata.get("host"), jsondata.get("port")

        # Adding contact
        if jsondata.get("host") and jsondata.get("port") and jsondata.get("id") and jsondata.get("public_key") and jsondata.get("type_crypto"):

            # stmt : statement
            stmt_surname = True if jsondata.get("surname") else "None"
            hostinfo_json = {'host': self.host, 'port': self.port}

            # convert b64 into encoded bytes public key
            jsondata["public_key"] = b64decode(jsondata["public_key"]).decode()

            accounts_lists = GetAccountsIdsFromHost(self.host, self.port)

            if not accounts_lists:
                try:
                    sender_id = self._adding_account()
                except Exception as e:
                    print(e)
                    raise e
            if accounts_lists:    
                sender_id = accounts_lists[0]

            AddContact(jsondata['id'], stmt_surname, sender_id, hostinfo_json, jsondata["public_key"], jsondata["type_crypto"])
        else:
            print('no valid contact')

    def adding_account(self, host: str, port: int):

        self.host, self.port = host, port

        account = self._adding_account()
