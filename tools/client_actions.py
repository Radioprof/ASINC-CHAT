import time
# from socket import socket, AF_INET, SOCK_STREAM

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
def send_user(to_user, msg, account='Guest'):
    """
    Формирование сообщения в чат
    :param to_user: кому предназначено сообщение
    :param msg: текст сообщения
    :param account: аккаунт отправителя
    :return:
    """
    data = {
        "action": 'send',
        "to_user": to_user,
        "time": time.time(),
        "message": msg,
        "from": account
        }
    return data


@log_call2
def listen_server(sock, my_account):
    """
    Прием сообщений в чате
    :param sock:
    :param my_account: имя пользователя
    :return:
    """
    # with socket(AF_INET, SOCK_STREAM) as sock:
    #     sock.connect(address)
    #     while True:
    data = sock.recv(1024).decode('utf-8')
    if 'action' in data and data['action'] == 'chat' and 'time' in data \
            and 'msg' in data and 'to_user' in data and data['to_user'] == my_account:
        print(f'Сообщение от {data["from"]}')
        print(f'{data["msg"]}')


@log_call2
def write_server(sock, my_name):
    """
    Отправка сообщения в чате на сервер
    :param sock:
    :param my_name: аккаунт отправителя
    :return:
    """
    # with socket(AF_INET, SOCK_STREAM) as sock:
    #     sock.connect(address)
    while True:
        todo = input('Ваши действия (exit/send): ')
        to = input('Кому: ')
        msg = input('Ваше сообщение: ')
        if todo == 'exit':
            break
        data = send_user(to, msg, my_name)
        sock.send(data.encode('utf-8'))
