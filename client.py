from socket import *
import json
import sys
import time


from log.client_log_config import client_log
from log.decor import log_call2
from tools.common import receive, send
# from tools.client_actions import presence


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
    client_log.info('Сообщение Presence серверу')
    return data


@log_call2
def main():
    try:
        host = sys.argv[1]
        port = int(sys.argv[2])
        if port < 1024 or port > 65535:
            raise ValueError
    except IndexError:
        host = 'localhost'
        port = 7777
    except ValueError:
        client_log.error('Номер порта может быть от 1024 до 65535.')
        sys.exit(1)
    s = socket(AF_INET, SOCK_STREAM)
    s.connect((host, port))
    data_presence = presence('Guest')
    send(data_presence, s)
    client_log.info(f'отправка сообщения: {data_presence}')
    data = receive(s)
    client_log.info('прием сообщения')
    client_log.info(f'Сообщение от сервера: {data}')
    s.close()


if __name__ == '__main__':
    main()
