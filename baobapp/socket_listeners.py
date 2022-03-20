import json
from os import listdir, path

from ownnetwork.utils import password_gen
from ownnetwork.baobap.api import NodeHostAPI
from ownnetwork.baobap.file_management import ManagementFile

def connect_all_accounts():
    
    socket_list = {}

    with open("db/accounts.json", 'r') as f:
        for key, value in json.load(f).items():
            try:
                server = NodeHostAPI(value['host'], value['port'], False)
                server.connect_account(key, value['password'])
                socket_list.update({key: {"server": server, "prv": value['private_key'], "puv": value['public_key'], "statut": True}})
            except RuntimeError as e:
                socket_list.update({key: {"server": server, "prv": value['private_key'], "puv": value['public_key'], "statut": False}})

    return socket_list


def disconnect_all_accounts(socket_list):
    
    for key, value in socket_list.items():
        if value['statut']:
            value['server'].s.close()

def get_all_sockets():

    ''' Creation of an indispensable variable to store the call nodes hosts that the client must request every X time to retrieve new data '''
    return connect_all_accounts()
