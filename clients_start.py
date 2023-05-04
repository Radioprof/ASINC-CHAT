import sys
from subprocess import Popen, CREATE_NEW_CONSOLE


def start_clients(filenm, client_quant):
    """

    :param filenm: имя, запускаемого файла
    :param client_quant: кол-во запускаемых приложений
    :return:
    """
    p_list = []
    while True:
        print(filenm, client_quant)
        user = input(f"Запустить {client_quant} клиентов {filenm} (s) / Закрыть клиентов (x) / Выйти (q) ")
        if user == 'q':
            break
        elif user == 's':
            for _ in range(int(client_quant)):
                p_list.append(Popen(f'python {filenm}', creationflags=CREATE_NEW_CONSOLE))
            print(' Запущено 3 клиента')
        elif user == 'x':
            for p in p_list:
                p.kill()
            p_list.clear()


if __name__ == '__main__':
    filename = sys.argv[1]
    quantity = sys.argv[2]
    start_clients(filename, quantity)
