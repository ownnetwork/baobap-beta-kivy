import requests
import json

class StatementContactLink():

    def __new__(self, link: str):

        if link.startswith("https://"):

            data_from_link = requests.get(link)
            data_from_link = json.loads(data_from_link.text.replace("'", '"'))

            if data_from_link:
                return data_from_link
            else:
                return False

        else:
            raise ValueError("The link must be in https, not on http")
