import threading
import time
from socket import *
import sys



from log.client_log_config import client_log
# from log.decor import log_call2
# from tools.common import receive, send
from tools.client_actions import listen_server, write_server, presence
from tools.common import send, receive
from client_db import ClientDatabase


def contacts_list_request(sock, name):
    req = {
        'action': 'get_contact',
        'time': time.time(),
        'user': name
    }
    send(sock, req)
    ans = receive(sock)
    if 'response' in ans and ans['response'] == 202:
        return ans['list_info']
    else:
        raise ServerError


# Функция добавления пользователя в контакт лист
def add_contact(sock, username, contact):
    req = {
        'action': 'add',
        'time': time.time(),
        'user': username,
        'account_name': contact
    }
    send(req, sock)
    ans = receive(sock)
    if 'response' in ans and ans['response'] == 200:
        pass
    else:
        raise ServerError('Ошибка создания контакта')
    print('Удачное создание контакта.')


# Функция запроса списка известных пользователей
def user_list_request(sock, username):
    req = {
        'action': 'users_reqwest',
        'time': time.time(),
        'account_name': username
    }
    send(sock, req)
    ans = receive(sock)
    if 'response' in ans and ans['response'] == 202:
        return ans['list_info']
    else:
        raise ServerError


# Функция удаления пользователя из контакт листа
def remove_contact(sock, username, contact):
    req = {
        'action': 'remove_contact',
        'time': time.time(),
        'user': username,
        'account_name': contact
    }
    send(sock, req)
    ans = receive(sock)
    if 'response' in ans and ans['response'] == 200:
        pass
    else:
        raise ServerError('Ошибка удаления клиента')
    print('Удачное удаление')


def database_load(sock, database, username):
    # Загружаем список известных пользователей
    try:
        users_list = user_list_request(sock, username)
    except ServerError:
        pass
    else:
        database.add_users(users_list)

    # Загружаем список контактов
    try:
        contacts_list = contacts_list_request(sock, username)
    except ServerError:
        pass
    else:
        for contact in contacts_list:
            database.add_contact(contact)


# @log_call2
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
    try:
        s = socket(AF_INET, SOCK_STREAM)
        s.connect((host, port))
        my_name = input('Введите имя пользователя: ')
        data_presence = presence(my_name)
        send(data_presence, s)
        answ_serv = receive(s)
        print(answ_serv)
    except:
        print(f'Не удалось установить соединение')
    # data_presence = presence(my_name)
    # send(data_presence, s)
    # client_log.info(f'отправка сообщения: {data_presence}')
    # data = receive(s)
    # client_log.info('прием сообщения')
    # client_log.info(f'Сообщение от сервера: {data}')
    else:
        database = ClientDatabase(my_name)
        database_load(s, database, my_name)
        # Watchdog основной цикл, если один из потоков завершён, то значит или потеряно соединение или пользователь
        # ввёл exit. Поскольку все события обрабатываются в потоках, достаточно просто завершить цикл.
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


if __name__ == '__main__':
    main()
