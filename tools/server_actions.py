import binascii
import hashlib
from socket import socket

from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QMessageBox

from log.decor import log_call
from log.server_log_config import serv_log
from tools.common import send, receive


class RegisterUser(QDialog):
    def __init__(self, database, server):
        super().__init__()

        self.database = database
        self.server = server

        self.setWindowTitle('Регистрация')
        self.setFixedSize(175, 183)
        self.setModal(True)
        self.setAttribute(Qt.WA_DeleteOnClose)

        self.label_username = QLabel('Введите имя пользователя:', self)
        self.label_username.move(10, 10)
        self.label_username.setFixedSize(150, 15)

        self.client_name = QLineEdit(self)
        self.client_name.setFixedSize(154, 20)
        self.client_name.move(10, 30)

        self.label_passwd = QLabel('Введите пароль:', self)
        self.label_passwd.move(10, 55)
        self.label_passwd.setFixedSize(150, 15)

        self.client_passwd = QLineEdit(self)
        self.client_passwd.setFixedSize(154, 20)
        self.client_passwd.move(10, 75)
        self.client_passwd.setEchoMode(QLineEdit.Password)
        self.label_conf = QLabel('Введите подтверждение:', self)
        self.label_conf.move(10, 100)
        self.label_conf.setFixedSize(150, 15)

        self.client_conf = QLineEdit(self)
        self.client_conf.setFixedSize(154, 20)
        self.client_conf.move(10, 120)
        self.client_conf.setEchoMode(QLineEdit.Password)

        self.btn_ok = QPushButton('Сохранить', self)
        self.btn_ok.move(10, 150)
        self.btn_ok.clicked.connect(self.save_data)

        self.btn_cancel = QPushButton('Выход', self)
        self.btn_cancel.move(90, 150)
        self.btn_cancel.clicked.connect(self.close)

        self.messages = QMessageBox()

        self.show()

    def save_data(self):
        if not self.client_name.text():
            self.messages.critical(
                self, 'Ошибка', 'Не указано имя пользователя.')
            return
        elif self.client_passwd.text() != self.client_conf.text():
            self.messages.critical(
                self, 'Ошибка', 'Введённые пароли не совпадают.')
            return
        elif self.database.check_user(self.client_name.text()):
            self.messages.critical(
                self, 'Ошибка', 'Пользователь уже существует.')
            return
        else:
            passwd_bytes = self.client_passwd.text().encode('utf-8')
            salt = self.client_name.text().lower().encode('utf-8')
            passwd_hash = hashlib.pbkdf2_hmac(
                'sha512', passwd_bytes, salt, 10000)
            self.database.add_user(
                self.client_name.text(),
                binascii.hexlify(passwd_hash))
            self.messages.information(
                self, 'Успех', 'Пользователь успешно зарегистрирован.')
            self.server.service_update_lists()
            self.close()


def login_required(func):
    def checker(*args, **kwargs):
        from server_loop import Server
        if isinstance(args[0], Server):
            found = False
            for arg in args:
                if isinstance(arg, socket):
                    for client in args[0].names:
                        if args[0].names[client] == arg:
                            found = True
            for arg in args:
                if isinstance(arg, dict):
                    if 'action' in arg and arg['action'] == 'presence':
                        found = True
            if not found:
                raise TypeError
        return func(*args, **kwargs)
    return checker


@log_call
def answer_message(message):
    if 'action' in message and message['action'] == 'presence' and 'time' in message \
            and 'user' in message and message['user']['account_name'] == 'Guest':
        serv_log.info('соединение установлено, код 200')
        return {'response': 200}
    serv_log.error('соединение не установлено, код 400')
    return {
        'response': 400,
        'error': 'Bad Request'
    }


@log_call
def chat_message(message):
    if 'action' in message and message['action'] == 'chat' and 'time' in message \
            and 'msg' in message and 'to_user' in message:
        serv_log.info('соединение установлено, код 200')
        return {'response': 200}
    serv_log.error('соединение не установлено, код 400')
    return {
        'response': 400,
        'error': 'Bad Request'
    }


@login_required
def message_from_client(message, messages_list, client, clients, names, database):

    if 'action' in message and message['action'] == 'presence' and \
            'time' in message and 'user' in message:
        if message['user']['account_name'] not in names.keys():
            names[message['user']['account_name']] = client
            resp = {'response': 200}
            send(resp, client)
        else:
            resp = {'response': 400}
            resp['error'] = 'Имя пользователя уже занято.'
            send(resp, client)
            clients.remove(client)
            client.close()
        return
    elif 'action' in message and message['action'] == 'send' and \
            'to_user' in message and 'time' in message \
            and 'from' in message and 'message' in message:
        messages_list.append(message)
        return
    elif 'action' in message and message['action'] == 'get_contact' and 'user' in message and \
            names[message['user']] == client:
        resp = {'response': 200}
        resp['list_info'] = database.get_contacts(message['user'])
        send(client, resp)

    elif 'action' in message and message['action'] == 'add_contact' and 'account_name' in message \
            and 'user' in message and names[message['user']] == client:
        database.add_contact(message['user'], message['account_name'])
        send(client, {'response': 200})

    elif 'action' in message and message['action'] == 'remove_contact' and 'account_name' in message \
            and 'user' in message and names[message['user']] == client:
        database.remove_contact(message['user'], message['account_name'])
        send(client, {'response': 200})

    elif 'action' in message and message['action'] == 'user_reqwest' and 'account_name' in message \
            and names[message['account_name']] == client:
        resp = {'response': 200}
        resp['list_info'] = [user[0] for user in database.users_list()]
        send(client, resp)

    else:
        resp = {'response': 400}
        resp['error'] = 'Запрос некорректен.'
        send(resp, client)
        return


def proc_message(message, names, listen_socks):
    if message['to_user'] in names and names[message['to_user']] in listen_socks:
        send(message, names[message['to_user']])
    elif message['to_user'] in names and names[message['to_user']] not in listen_socks:
        raise ConnectionError
    else:
        print(f'Пользователь {message["to_user"]} не зарегистрирован на сервере, отправка сообщения невозможна.')
