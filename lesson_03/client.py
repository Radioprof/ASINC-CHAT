from socket import *
import json
import sys

from tools.common import receive, send
from tools.client_actions import presence


def client_status(subject):
    status = json.dumps(subject, indent=4)
    return status


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
        print('Номер порта может быть от 1024 до 65535.')
        sys.exit(1)
    s = socket(AF_INET, SOCK_STREAM)
    s.connect((host, port))
    data_presence = presence('Guest')
    send(data_presence, s)
    data = receive(s)
    print('Сообщение от сервера: ', data)
    s.close()


if __name__ == '__main__':
    main()
