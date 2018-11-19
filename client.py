#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Programa cliente que abre un socket a un servidor
"""

import socket
import sys

METHOD = ""
# Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as my_socket:
    my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    if len(sys.argv) == 3:
        METHOD = sys.argv[1]
        USER = sys.argv[2].split("@")[0]
        IP = sys.argv[2].split("@")[1].split(":")[0]
        PORT = sys.argv[2].split("@")[1].split(":")[1]

        #  my_socket.connect((IP, PORT))
        my_socket.connect(('localhost', 6001))
        my_socket.send(bytes(METHOD + " sip:" + USER + "@" + IP +
                        " SIP/2.0", 'utf-8') + b'\r\n\r\n')
    else:
        print("Usage: python3 client.py method receiver@IP:SIPport")


    data = my_socket.recv(1024)
    Number_data = data.decode('utf-8').split(" ")[1]
    print(Number_data)

    if Number_data == "100":
        my_socket.send(bytes("ACK" + " sip:" + USER + "@" + IP +
                        " SIP/2.0", 'utf-8') + b'\r\n\r\n')
    else:
        print('Recibido -- ', data.decode('utf-8'))
    print("Terminando socket...")

print("Fin.")
