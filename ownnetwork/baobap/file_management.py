# MIT License -> LISCENCE.mit

from ownnetwork.baobap.models.crypto.generate_key import GenerateKey
from ownnetwork.utils import uuid_to_hex

from os import makedirs, path
import json
from base64 import b64decode

class ManagementFile():

    def __init__(self):
        pass

    def avatar_from_user_id_exist(self, account_type: str, account_id: str):
        if path.exists(f'db/img/avatar/{account_type}/{account_id}.png'):
            return f'db/img/avatar/{account_type}/{account_id}.png'
        
        elif not path.exists(f'db/img/avatar/{account_type}/{account_id}.png'):
            return 'db/img/avatar/default/default.png'

    def file_hostinfo(self, socket_list):
        host_list = {}

        with open("db/accounts.json", 'r') as f:
            account_data = json.load(f)

        for key, value in socket_list.items():
            host_with_port = value['server'].s.getpeername()[0] + '_' + str(value['server'].s.getpeername()[1])
            
            if not host_list.get(host_with_port):
                if value['statut']: 
                    data = value['server'].hostinfo()
                    
                    with open(f"db/img/hosts/node/{host_with_port}.png", 'wb') as logofile:
                        logofile.write(b64decode(data['logo']))

                    host_list.update({host_with_port: {'name': data['name'], 'statut': value['statut']}})


        return host_list

    def chat_id_from_user_id(self, user_id: str):
        with open("db/users.json", 'r') as f: return json.load(f)[user_id]['chat_id']

    def reset_file_setup(self):
        with open("db/accounts.json", 'w') as f:
            json.dump({}, f)

        with open("db/users.json", 'w') as f:
            json.dump({}, f)

        with open("db/settings.json", 'w') as f:
            json.dump({}, f)
