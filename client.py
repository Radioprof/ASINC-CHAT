import threading
import time
from socket import *
import sys


from log.client_log_config import client_log
from log.decor import log_call2
from tools.common import receive, send
from tools.client_actions import presence, listen_server, write_server


@log_call2
def main():
    try:
        host = sys.argv[1]
        port = int(sys.argv[2])
        if port < 1024 or port > 65535:
            raise ValueError
    except IndexError:
        host = 'localhost'
        port = 10000
    except ValueError:
        client_log.error('Номер порта может быть от 1024 до 65535.')
        sys.exit(1)
    s = socket(AF_INET, SOCK_STREAM)
    s.connect((host, port))
    my_name = input('Введите имя пользователя: ')
    # data_presence = presence(my_name)
    # send(data_presence, s)
    # client_log.info(f'отправка сообщения: {data_presence}')
    # data = receive(s)
    # client_log.info('прием сообщения')
    # client_log.info(f'Сообщение от сервера: {data}')
    receiver = threading.Thread(target=listen_server, args=(s, my_name))
    receiver.daemon = True
    receiver.start()

    # затем запускаем отправку сообщений и взаимодействие с пользователем.
    user_interface = threading.Thread(target=write_server, args=(s, my_name))
    user_interface.daemon = True
    user_interface.start()
    while True:
        time.sleep(1)
        if receiver.is_alive() and user_interface.is_alive():
            continue
        break
    # s.close()


if __name__ == '__main__':
    main()
