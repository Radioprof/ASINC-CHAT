import time

# from log.client_log_config import client_log
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
