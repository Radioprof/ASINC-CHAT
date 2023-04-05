def answer_message(message):
    if 'action' in message and message['action'] == 'presence' and 'time' in message \
            and 'user' in message and message['user']['account_name'] == 'Guest':
        return {'response': 200}
    return {
        'response': 400,
        'error': 'Bad Request'
    }
