import inspect
import logging
import traceback
from functools import wraps


def log_call(func):
    @wraps(func)
    def wr_deco(*args, **kwargs):
        logging.basicConfig(level=logging.DEBUG,
                            filename='call_function.log',
                            encoding='utf-8',
                            filemode='a',
                            format='%(asctime)s %(levelname)s - %(message)s')
        func_log = logging.getLogger('func_log')
        func_log.info(f'{func.__name__}, {func.__module__} '
                      f'Вызов из функции {traceback.format_stack()[0].strip().split()[-1]}. '
                      f'Вызов из функции {inspect.stack()[1][3]} '
                      f'{args} {kwargs}')
        return func(*args, **kwargs)
    return wr_deco


def log_call2(func):
    @wraps(func)
    def wr_deco(*args, **kwargs):
        logging.basicConfig(level=logging.DEBUG,
                            filename='call_function_client.log',
                            encoding='utf-8',
                            filemode='a',
                            format='%(asctime)s %(levelname)s %(message)s')
        func_log = logging.getLogger('func_log')
        func_log.info(f'{func.__name__}, {func.__module__} {args} {kwargs}')
        return func(*args, **kwargs)
    return wr_deco
