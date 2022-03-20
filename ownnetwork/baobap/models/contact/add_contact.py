# MIT License -> LISCENCE.mit

from ownnetwork.baobap.models.chat.generate_chat_identifier import GenerateChatIdentifier

from os import makedirs, path
import json

"""
Add a contact to the json contact file
"""
class AddContact(object):

    def __init__(self, account_id: str, surname: str, sender_id: str, hostinfo: dict, public_key, type_encryptation = 'RSA'):

        # prevent a interfering file with the creation of a folder

        account_id = account_id.replace('/','')

        if path.exists('db/users.json'):

            with open("db/users.json", 'r+') as f:
                content_json = json.load(f)

                # generate a chat id identifier, that create a file that is ready to be writing
                chat_id = GenerateChatIdentifier()

                if not content_json.get(account_id):

                    account_data = {
                        account_id: {
                            "surname": surname,
                            "host": hostinfo['host'],
                            "port": hostinfo['port'],
                            "public_key": public_key,
                            "type_crypto": type_encryptation,
                            "sender_id": sender_id,
                            "chat_id": chat_id
                            }
                        }

                    content_json.update(account_data)
                    f.seek(0) #allow to the return on first line from the json file
                    json.dump(content_json, f, indent=2)
