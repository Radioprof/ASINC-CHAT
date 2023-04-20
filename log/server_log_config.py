import logging.handlers

serv_log = logging.getLogger('server_log')
serv_log.setLevel(logging.DEBUG)
serv_log.propagate = False

serv_handler = logging.handlers.TimedRotatingFileHandler(filename='server.log', encoding='utf-8', when='D', interval=1)
formater = logging.Formatter('%(asctime)s %(levelname)s %(module)s %(message)s')
serv_handler.setFormatter(formater)
serv_log.addHandler(serv_handler)

# serv_log.warning('test server')
