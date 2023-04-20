import logging

logging.basicConfig(level=logging.DEBUG,
                    filename='client.log',
                    filemode='a',
                    format='%(asctime)s %(levelname)s %(module)s %(message)s')

logging.critical('test client')
