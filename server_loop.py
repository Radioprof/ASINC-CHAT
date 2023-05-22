import select
from socket import socket, AF_INET, SOCK_STREAM

from metaclass import ServerVerifier
from srv_descript import PortCheck
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


class Server(metaclass=ServerVerifier):
    port = PortCheck()

    def __init__(self, address, port):
        self.port = port
        self.address = address
        self.clients = []
        self.msgs = []
        self.accnt = {}

    def init_socket(self):
        s = socket(AF_INET, SOCK_STREAM)
        s.bind((self.address, self.port))
        s.settimeout(0.2)
        self.sock = s

        self.sock.listen()

    def main_loop(self):
        self.init_socket()
        while True:
            try:
                conn, addr = self.sock.accept()
            except OSError as e:
                pass
            else:
                print("Получен запрос на соединение от %s" % str(addr))
                self.clients.append(conn)
                print(self.clients)
            finally:
                wait = 10
                r = []
                w = []
                try:
                    if self.clients:
                        r, w, e = select.select(self.clients, self.clients, [], wait)
                except:
                    pass

            if r:
                for client_with_message in r:
                    try:
                        ms = receive(client_with_message)
                        message_from_client(ms, self.msgs, client_with_message, self.clients, self.accnt)
                    except Exception:
                        self.clients.remove(client_with_message)
            for i in self.msgs:
                try:
                    proc_message(i, self.accnt, w)
                except Exception:
                    self.clients.remove(self.accnt[i['to_user']])
                    del self.accnt[i['to_user']]
            self.msgs.clear()


def main():
    server = Server('', 10000)
    server.main_loop()
    print('Эхо-сервер запущен!')

if __name__ == '__main__':
    main()
