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

print('\n***  Проверка всех зеркал одновременно, 9 положений по очереди, начиная с нулеового  ***\n')
id = input('Введите № платы, которую хотите проверить (от 1 до 3) и нажмите Enter: ')
id = int(id)
sock.connect(('192.168.1.10{}'.format(id-1), 502))
print('Подключились, IP: 192.168.1.10{}'.format(id-1))

print('\nДалее каждое нажатие Enter начнет поворачивать все зеркала в новое положение:')

pos_num = [0, 2, 4, 7, 3, 1, 5, 8, 6, 0]
pos_descr = ['Нулевое', 'Вверх', 'Вверх/вправо', 'Вправо', 'Вниз/вправо','Вниз', 'Вниз/влево', 'Влево', 'Вверх/влево', 'Нулевое']
# 

for pos in range(10):
    while(input()): pass
    print('{} - {}'.format(pos_num[pos], pos_descr[pos]))

    data = [int('0x0{}0{}'.format(pos_num[pos], pos_num[pos]),16) for i in range(72)]
    message = tcp.write_multiple_registers(slave_id=id, starting_address=0, values=data[:28])
    response = tcp.send_message(message, sock)
    message = tcp.write_multiple_registers(slave_id=id, starting_address=28, values=data[28:])
    response = tcp.send_message(message, sock)
    

sock.close()