#!/usr/bin/env python
# scripts/examples/simple_tcp_client.py
#  https://umodbus.readthedocs.io/en/latest/index.html
import socket
import os
import time
import traceback

from umodbus import conf
from umodbus.client import tcp


HOST = '192.168.1.100'
PORT = 502
slave_id = 1
trig = True

client_stop = False
client_connected = False

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def send_72_holding_reg(ip, port, slave_id, data):
    # print('\n\tWriting data to slave {}, id={}'.format(ip, slave_id))
    # print(len(data))
    
    # Enable values to be signed (default is False).
    conf.SIGNED_VALUES = True

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.3)
    try:
        sock.connect((ip, port))

        temp_h = []
        temp = []

        for i in range(len(data)):
            for j in range(8*3):
                h = '0x0' + data[i][j*2+1] + '0' + data[i][j*2]
                temp_h.append(h)
                temp.append(int(h, 16))

        # FIXME - смотри fix.txt
        # кратко - 28-ой регистр глючит если писать все сразу. Пэтому вначале пишем все до 28 (0..27), а потом с 28-го до конца (28..72)
        message = tcp.write_multiple_registers(slave_id=slave_id, starting_address=0, values=temp[0:28])
        response = tcp.send_message(message, sock)

        message = tcp.write_multiple_registers(slave_id=slave_id, starting_address=28, values=temp[28:])
        response = tcp.send_message(message, sock)
    
    except Exception as e:
        print('--send_data_to_slave {}--> error:'.format(ip))
        print(traceback.format_exc())
        sock.close()
    
    else:
        sock.shutdown(socket.SHUT_WR)
        sock.close()


def reconnect():
    global client_connected, sock

    try:
        sock.close()
    except Exception as e:
        time.sleep(1)
    else:
        time.sleep(0.1)
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.5)

    try:
        sock.connect((HOST, PORT))
    except Exception as e:
        time.sleep(0.1)
    else:
        client_connected = True
        print('\n\tConnected to {}, id={}'.format(HOST, slave_id))


def client_main(q_in, q_out, ip, port, id, sleep_time):
    global client_stop, HOST, PORT, slave_id, client_connected, sock

    HOST, PORT, slave_id = ip, port, id

    print('--modBus_client--> PID:', os.getpid())

    # main client loop
    while client_stop == False:
        # check queue
        if q_in.empty() == False:
            input_q = q_in.get()
            
            if input_q == '' or None:
                pass

            elif input_q == 'stop':
                print('--modBus_client---> signal {}'.format(input_q))
                client_stop = True
                print('\n--modBus_client---> Stopped'.format())
                print('--------------------------------------------------------')

            elif input_q[0] == 'send_data':
                # communicate
                data = input_q[1]
                send_72_holding_reg(ip, port, slave_id, data)

                q_out.put('q')
                
            else:
                print('--client_for_dashboard_server_robot--> unknown comand'.format())

        else:
            time.sleep(sleep_time)