# MIT License -> LISCENCE.mit

from os import makedirs, path
import json

"""
Change value from a json file
"""
class JsonModifier(object):

    def __init__(self, directory):

        self.directory = directory + '.json'

    def rename(self, value1, value2, tovalue):

        with open(self.directory, 'r+') as f:
            content_json = json.load(f)

            content_json[value1][value2] = tovalue

            json.dump('{}', f, indent=2)

        with open(self.directory, 'w+') as f:
            
            json.dump(content_json, f, indent=2)
