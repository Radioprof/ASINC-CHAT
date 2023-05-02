import select
from socket import socket, AF_INET, SOCK_STREAM

from tools.common import receive
from tools.server_actions import message_from_client, proc_message


def read_requests(r_clients, all_clients):
    responses = {}
    for sock in r_clients:
        try:
            data = sock.recv(1024).decode('utf-8')
            responses[sock] = data
        except:
            print('Клиент {} {} отключился'.format(sock.fileno(), sock.getpeername()))
            all_clients.remove(sock)
    return responses


def write_responses(requests, w_clients, all_clients):
    for sock in w_clients:
        if sock in requests:
            try:
                resp = requests[sock].encode('utf-8')
                for _sock in w_clients:
                    _sock.send(resp.upper())
            except:
                print('Клиент {} {} отключился'.format(sock.fileno(), sock.getpeername()))
                sock.close()
                all_clients.remove(sock)



def mainloop():
    address = ('', 10000)
    clients = []
    msgs = []
    accnt = {}
    s = socket(AF_INET, SOCK_STREAM)
    s.bind(address)
    s.listen(10)
    s.settimeout(0.2)
    while True:
        try:
            conn, addr = s.accept()
        except OSError as e:
            pass
        else:
            print("Получен запрос на соединение от %s" % str(addr))
            clients.append(conn)
            print(clients)
        finally:
            wait = 10
            r = []
            w = []
            try:
                if clients:
                    r, w, e = select.select(clients, clients, [], wait)
            except:
                pass

            if r:
                for client_with_message in r:
                    try:
                        ms = receive(client_with_message)
                        message_from_client(ms, msgs, client_with_message, clients, accnt)
                    except Exception:
                        clients.remove(client_with_message)
            for i in msgs:
                try:
                    proc_message(i, accnt, w)
                except Exception:
                    clients.remove(accnt[i['to_user']])
                    del accnt[i['to_user']]
            msgs.clear()


print('Эхо-сервер запущен!')
mainloop()
