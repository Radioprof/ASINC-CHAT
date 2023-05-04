import subprocess
import ipaddress
from tabulate import tabulate
from chardet import detect


def dec_ping(addr):
    p = subprocess.Popen(f'ping {addr}', stdout=subprocess.PIPE)
    out = p.stdout.read()
    det_ping = detect(out)['encoding']
    s = out.decode(det_ping).encode('utf-8')
    r = s.decode('utf-8')
    return r


def res_ping(addr):
    r = dec_ping(addr)
    if 'Заданный узел недоступен' in r:
        print(f'Узел {addr} не доступен')
    else:
        print(f'Узел {addr} доступен')


def host_ping(ip_list):
    for addr in ip_list:
        ipv4 = ipaddress.ip_address(addr)
        res_ping(ipv4)
    return


def host_range_ping(host_addr='192.168.1.0/24'):
    subnet = ipaddress.ip_network(host_addr)
    for i in range(2):
        res_ping(subnet[i+1])
    return


def host_range_ping_tab(host_addr='192.168.1.0/24'):
    subnet = ipaddress.ip_network(host_addr)
    ip_tab_list = []
    for i in range(2):
        r = dec_ping(subnet[i+1])
        if 'Заданный узел недоступен' in r:
            ip_tab_list.append({'Unreachable': subnet[i+1]})
        else:
            ip_tab_list.append({'Reachable': subnet[i+1]})
    print(tabulate(ip_tab_list, headers='keys'))
    return


iplist = ('192.168.0.1', '192.168.0.2')
host_ping(iplist)
host_range_ping('192.168.0.0/24')
host_range_ping_tab('192.168.0.0/24')
