#!/usr/bin/env python
# scripts/examples/simple_tcp_client.py
#  https://umodbus.readthedocs.io/en/latest/index.html
import socket
import time

from umodbus import conf
from umodbus.client import tcp

# Enable values to be signed (default is False).
conf.SIGNED_VALUES = True

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.settimeout(2)

print('\n***  Проверка зеркал по одному, начиная с первого  ***\n')
id = input('Введите № платы, которую хотите проверить (от 1 до 3) и нажмите Enter: ')
id = int(id)
sock.connect(('192.168.1.10{}'.format(id-1), 502))
print('Подключились, IP: 192.168.1.10{}'.format(id-1))

data = [int('0x0{}0{}'.format(0, 0),16) for i in range(72)]
message = tcp.write_multiple_registers(slave_id=id, starting_address=0, values=data[:28])
response = tcp.send_message(message, sock)
message = tcp.write_multiple_registers(slave_id=id, starting_address=28, values=data[28:])
response = tcp.send_message(message, sock)
print('\nПовернули все зеркала в нулевое положение')

print('\nДалее каждое нажатие Enter начнет поворачивать по одному зеркалу, начиная с первого:')
pos = 4 # в  какое положение крутим
for i in range(72):
    while(input()): pass
    print('Зеркало {} (регистр {}, Правая часть)'.format((i+1)*2 - 1, i))
    h = '0x0{}0{}'.format(0, 4)
    temp = int(h, 16)
    message = tcp.write_single_register(slave_id=id, address=i, value=temp)
    response = tcp.send_message(message, sock)

    while(input()): pass
    print('Зеркало {} (регистр {}, Левая часть)'.format((i+1)*2, i))
    h = '0x0{}0{}'.format(4, 4)
    temp = int(h, 16)
    message = tcp.write_single_register(slave_id=id, address=i, value=temp)
    response = tcp.send_message(message, sock)



sock.close()