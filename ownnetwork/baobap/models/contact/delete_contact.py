# MIT License -> LISCENCE.mit

import json

"""
Delete a contact from json acccount file
"""
class DeleteContact(object):

    def __init__(self, contact_id: str):
        
        with open("db/users.json", 'r+') as f:
            content_json = json.load(f)

            if content_json.get(contact_id):
                del content_json[contact_id]
                #content_json.remove(contact_id)
            json.dump('{}', f, indent=2)

        with open("db/users.json", 'w+') as f:
            
            json.dump(content_json, f, indent=2)