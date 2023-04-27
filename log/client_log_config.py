import logging

client_log = logging.getLogger('client_log')
client_log.setLevel(logging.DEBUG)
client_log.propagate = False
_format = logging.Formatter('%(asctime)s %(levelname)s %(module)s %(message)s')
client_handler = logging.FileHandler(filename='./logfile/client.log', encoding='utf-8', mode='a')
client_handler.setFormatter(_format)
client_log.addHandler(client_handler)
