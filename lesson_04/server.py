from socket import *
import sys

from tools.common import receive, send
from tools.server_actions import answer_message


def main():
    s = socket(AF_INET, SOCK_STREAM)
    if '-p' in sys.argv:
        port = int(sys.argv[sys.argv.index('-p') + 1])
    else:
        port = 7777
    if '-a' in sys.argv:
        address = sys.argv[sys.argv.index('-a') + 1]
    else:
        address = ''
    s.bind((address, port))
    s.listen(5)
    while True:
        client, addr = s.accept()
        data = receive(client)
        print('Сообщение: ', data, ', было отправлено клиентом: ', addr)
        msg = answer_message(data)
        send(msg, client)
        client.close()


if __name__ == '__main__':
    main()
