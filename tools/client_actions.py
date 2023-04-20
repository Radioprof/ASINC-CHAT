import time

from log.client_log_config import client_log


def auth(name, password):
    data = {
        "action": "authenticate",
        "time": time.time(),
        "user": {
            "account_name": name,
            "password": password
            }
        }
    client_log.info('Сообщение Authenticate серверу')
    return data


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
