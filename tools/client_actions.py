import time
from socket import socket, AF_INET, SOCK_STREAM

from log.decor import log_call2


@log_call2
def auth(name, password):
    data = {
        "action": "authenticate",
        "time": time.time(),
        "user": {
            "account_name": name,
            "password": password
            }
        }
    return data


@log_call2
def presence(name, status_mes=None):
    data = {
        "action": "presence",
        "time": time.time(),
        "type": "status",
        "user": {
            "account_name": name,
            "status": status_mes
            }
        }
    return data


@log_call2
def listen_server(address):
    with socket(AF_INET, SOCK_STREAM) as sock:
        sock.connect(address)
        while True:
            print('Прием')
            data = sock.recv(1024).decode('utf-8')
            print(data)


@log_call2
def write_server(address):
    with socket(AF_INET, SOCK_STREAM) as sock:
        sock.connect(address)
        while True:
            msg = input('Ваше сообщение: ')
            if msg == 'exit':
                break
            sock.send(msg.encode('utf-8'))
