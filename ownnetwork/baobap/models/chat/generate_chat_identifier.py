# MIT License -> LISCENCE.mit

from os import path
import json
from uuid import uuid1

"""
Generate a unique identifier to store the data of a conversation
"""
class GenerateChatIdentifier(object):

    def __new__(self):

        id_chat = uuid1().hex
        file_path = f'db/chat/{id_chat}.json'

        if not path.exists(file_path):
            with open(file_path, 'w') as f:
                json.dump({}, f)
            return id_chat
        elif path.exists(file_path):
            return self.__init__()
