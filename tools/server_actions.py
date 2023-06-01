from log.decor import log_call
from log.server_log_config import serv_log
from tools.common import send


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

    elif 'action' in message and message['action'] == 'add_contact' and 'account_name' in message and 'user' in message \
            and names[message['user']] == client:
        database.add_contact(message['user'], message['account_name'])
        send(client, {'response': 200})

    elif 'action' in message and message['action'] == 'remove_contact' and 'account_name' in message and 'user' in message \
            and names[message['user']] == client:
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
