import json

from log.decor import log_call


@log_call
def receive(source):
    res_data = source.recv(1024)
    dec_data = res_data.decode('utf-8')
    data = json.loads(dec_data)
    return data


@log_call
def send(message, target):
    data = json.dumps(message, indent=4)
    target.send(data.encode('utf-8'))
    return
