# MIT License -> LISCENCE.mit

from ownnetwork.baobap.models.crypto.universal import UNIVERSALCrypto

from socket import socket, AF_INET, SOCK_STREAM, gethostname, error as socket_error, gaierror
import socks
import json
from base64 import b64encode
import errno

"""
# WORKING
Routing data with ONION Tor routing
"""
class OnionRouting():
    
    def __new__(self):
        socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 9050, True)
        s = socks.socksocket()
        return s

"""
Default node-host BaoBapp API
""" 
class NodeHostAPI():

    def __init__(self, host: str, port: int, timeout = False):
        if not host:
            host = '192.168.1.94'
        self.host = host
        self.port = port
        self.max_len_recv = 10240
        self.timeout = False
        try:
            # WORKING
            # socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, self.host, self.port, True)
            # socket = socks.socksocket
            s = socket(AF_INET, SOCK_STREAM)
            s.connect((self.host, self.port))
            s.settimeout(timeout)
            self.s = s
        except gaierror as e:
            print(e)
        except socket_error as e:
            print(e)

    """
    Receving data
    """
    def recv(self, attempt_d):
        if self.timeout == True:
            try:
                while True:
                    d = self.s.recv(self.max_len_recv).decode('utf-8')
                    if attempt_d in d: return json.loads(d)
            except:
                pass
        elif self.timeout == False or 0:
            while True:
                try:
                    d = self.s.recv(self.max_len_recv).decode('utf-8')
                    if attempt_d in d: return json.loads(d)
                except:
                    pass

    def get_data(self):
        return self.recv('get-data')

    def async_get_data(self, attempt_d):
        try:
            d = self.s.recv(self.max_len_recv).decode('utf-8')
            if attempt_d in d:
                return json.loads(d)
        except:
            pass

    def create_new_account(self, password: str):
        add_user_block = {'register_pass': password}
        self.send_data(add_user_block)
        return self.recv('user_id_register')['user_id_register']

    def connect_account(self, user_id: str, password: str):
        user_data = {
            'auth_user_id': user_id,
            'pswd': password
        }
        self.send_data(user_data)

    """
    send data to contact id (string data)
    """
    def message(self, to_user_id: str, msg: str, public_key: str):
        msg = b64encode(UNIVERSALCrypto().encrypt_data(public_key, json.dumps({'message': msg}).encode())).decode()
        send_to = {
            'send_data_to': to_user_id,
            'data': msg
        }
        self.send_data(send_to)

    def hostinfo(self):
        hostinfo = {'hostinfo': ''}
        number = 20

        self.send_data(hostinfo)

        self.max_len_recv = self.max_len_recv * number
        return self.recv('logo')
        self.max_len_recv = self.max_len_recv / number

    def send_data(self, d):
        try:
            self.s.send(json.dumps(d).encode())
        except AttributeError as error:
            raise RuntimeError('Failed to send message to transfer host') from error
        except:
            pass
