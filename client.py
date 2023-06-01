import threading
import time
import sys

from PyQt5.QtWidgets import QApplication

from gui.client import UserNameDialog, ClientTransport, ClientMainWindow
from tools.common import send, receive
from client_db import ClientDatabase
from tools.errors import ServerError


# def contacts_list_request(sock, name):
#     req = {
#         'action': 'get_contact',
#         'time': time.time(),
#         'user': name
#     }
#     send(sock, req)
#     ans = receive(sock)
#     if 'response' in ans and ans['response'] == 202:
#         return ans['list_info']
#     else:
#         raise ServerError
#
#
# # Функция добавления пользователя в контакт лист
# def add_contact(sock, username, contact):
#     req = {
#         'action': 'add',
#         'time': time.time(),
#         'user': username,
#         'account_name': contact
#     }
#     send(req, sock)
#     ans = receive(sock)
#     if 'response' in ans and ans['response'] == 200:
#         pass
#     else:
#         raise ServerError('Ошибка создания контакта')
#     print('Удачное создание контакта.')
#
#
# # Функция запроса списка известных пользователей
# def user_list_request(sock, username):
#     req = {
#         'action': 'users_reqwest',
#         'time': time.time(),
#         'account_name': username
#     }
#     send(sock, req)
#     ans = receive(sock)
#     if 'response' in ans and ans['response'] == 202:
#         return ans['list_info']
#     else:
#         raise ServerError
#
#
# # Функция удаления пользователя из контакт листа
# def remove_contact(sock, username, contact):
#     req = {
#         'action': 'remove_contact',
#         'time': time.time(),
#         'user': username,
#         'account_name': contact
#     }
#     send(sock, req)
#     ans = receive(sock)
#     if 'response' in ans and ans['response'] == 200:
#         pass
#     else:
#         raise ServerError('Ошибка удаления клиента')
#     print('Удачное удаление')
#
#
# def database_load(sock, database, username):
#     # Загружаем список известных пользователей
#     try:
#         users_list = user_list_request(sock, username)
#     except ServerError:
#         pass
#     else:
#         database.add_users(users_list)
#
#     try:
#         contacts_list = contacts_list_request(sock, username)
#     except ServerError:
#         pass
#     else:
#         for contact in contacts_list:
#             database.add_contact(contact)
#
#
# @log_call2
def main():
    host = sys.argv[1]
    port = int(sys.argv[2])
    client_app = QApplication(sys.argv)
    try:
        client_name = sys.argv[3]
    except:
        start_dialog = UserNameDialog()
        client_app.exec_()
        if start_dialog.ok_pressed:
            client_name = start_dialog.client_name.text()
            del start_dialog
        else:
            exit(0)

    database = ClientDatabase(client_name)

    try:
        transport = ClientTransport(port, host, database, client_name)
    except ServerError as error:
        print(error.text)
        exit(1)
    transport.setDaemon(True)
    transport.start()

    main_window = ClientMainWindow(database, transport)
    main_window.make_connection(transport)
    main_window.setWindowTitle(f'Чат Программа alpha release - {client_name}')
    client_app.exec_()

    transport.transport_shutdown()
    transport.join()


if __name__ == '__main__':
    main()
