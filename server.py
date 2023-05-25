from socket import *
import sys

from log.decor import log_call
from log.server_log_config import serv_log
from tools.common import receive, send
from tools.server_actions import answer_message

@log_call
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
        serv_log.info('прием сообщения')
        serv_log.info(f'Сообщение: {data} было отправлено клиентом:  {addr}')
        msg = answer_message(data)
        send(msg, client)
        serv_log.info(f'отправка сообщения: {msg}')
        client.close()


if __name__ == '__main__':
    main()
