# side libs
import time
import os
import queue
import socket
import traceback
import configparser

from umodbus import conf
from umodbus.client import tcp
from datetime import datetime
from multiprocessing import *

# project libs
import modBus_client


# main programm part
if __name__ == '__main__':
    try:
        print('mirror_modBus_master PID:', os.getpid())

        # starting separate process for each of 3 modbus TCP clients
        q0_in = Queue()
        q0_out = Queue()
        proc0 = Process(target = modBus_client.client_main, name = 'clent_for_slave', args = (q0_out, q0_in, '192.168.1.100', 502, 1, 0.05))
        # proc0 = Process(target = modBus_client.client_main, name = 'clent_for_slave', args = (q0_out, q0_in, '127.000.000.001', 502, 1, 0.05))
        proc0.start()

        q1_in = Queue()
        q1_out = Queue()
        proc1 = Process(target = modBus_client.client_main, name = 'clent_for_slave', args = (q1_out, q1_in, '192.168.1.101', 502, 2, 0.05))
        proc1.start()

        q2_in = Queue()
        q2_out = Queue()
        proc2 = Process(target = modBus_client.client_main, name = 'clent_for_slave', args = (q2_out, q2_in, '192.168.1.102', 502, 3, 0.05))
        proc2.start()
        

        # starting server for incoming data form Unity
        HOST = '127.0.0.13'   
        PORT = 5555           
        connected = False
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            try:
                sock.bind((HOST, PORT))
                sock.listen()
                print('\n--------------------------------------------------------')
                print('--server_for_unity--> start listening on {} ...'.format((HOST, PORT)))

                
                while connected == False:
                    try:
                        conn, addr = sock.accept()
                    except Exception as e:                       
                        pass

                    else:
                        print('--server_for_unity--> Connected with {} ...'.format(addr))

                    connected = True
                
                
                # main server loop
                while True:
                    try:
                        temp = conn.recv(1024).decode("utf-8")

                    except Exception as e:
                        print('--server_for_unity--> error recv or send:\n{}'.format(e))

                    try:
                        # print('\n-------------- New data to slaves --------------')
                        # print('--server_for_unity--> data from Unity: {}'.format(temp))
                        # print('--server_for_unity--> data from Unity: {}'.format(temp))
                        # print(type(temp))
                        data_in = temp.split()
                        # print('\tdata_in = {}'.format(data_in))
                        # print(len(data_in))
                        # print(data_in[0], len(data_in[0]))

                        data_in += ['0000000000000000']

                        data_new = [ [data_in[j+i+0] + data_in[j+i+1] + data_in[j+i+2] for i in range(0, 9, 3)] for j in range(0, 27, 9) ]

                        try:
                            q0_out.put(['send_data', data_new[0]])
                            q1_out.put(['send_data', data_new[1]])
                            q2_out.put(['send_data', data_new[2]])

                            conn.sendall('1'.encode())

                        except Exception as e:
                            print('--server_for_unity--> error data processing:'.format())
                            print(traceback.format_exc())
                    
                    except Exception as e:
                        print('--server_for_unity--> error data processing:'.format())
                        print(traceback.format_exc())
                    else:
                        pass

            except Exception as e:
                # print('Timeout!')
                print('--server_for_unity--> error----:\n{}'.format(e))
                time.sleep(2)
                sock.close()
  

    except Exception as e:
        try: 
            q0_out.put('stop')
            q1_out.put('stop')
            q2_out.put('stop')
            
            time.sleep(3)
            proc0.terminate()
            proc1.terminate()
            proc2.terminate()
            pass 
        except: print('')
        
        print('\n--------- MAIN PROGRAM ERROR ---------------------\n')
        print(traceback.format_exc())
        print('Please, close all program\'s windows, wait 10 s, and try again')