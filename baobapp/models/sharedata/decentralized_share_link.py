import requests
import siaskynet as skynet
from kivymd.toast import toast
from ..exeptions import NoInternetConnection

def skynet_link(data: str):
    client = skynet.SkynetClient()
    skylink = client.upload({'data' : data})
    return 'https://siasky.net/' + skylink[6:]

class DecentralizedShareLink():

    def __new__(self, data: str):
        try:
            return skynet_link(data)
        except:
            raise NoInternetConnection()