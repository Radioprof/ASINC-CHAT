import subprocess
import ipaddress
from subprocess import CREATE_NEW_CONSOLE


def host_ping(host_addr='192.168.1.0/24'):
    subnet = ipaddress.ip_network('192.168.0.0/24')
    for i in range(2):
        # print(subnet[i+1])
        p = subprocess.Popen(f'ping {subnet[1]}', creationflags=CREATE_NEW_CONSOLE)
        print(type(p))
    return


host_ping()
