from log.decor import log_call
from log.server_log_config import serv_log


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
