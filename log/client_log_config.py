import logging

logging.basicConfig(level=logging.DEBUG,
                    filename='client.log',
                    encoding='utf-8',
                    filemode='a',
                    format='%(asctime)s %(levelname)s %(module)s %(message)s')

client_log = logging.getLogger('client_log')

# client_log.warning('test client')
