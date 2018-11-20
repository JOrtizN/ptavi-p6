#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Programa cliente que abre un socket a un servidor."""

import socket
import sys

METHOD = ""
# Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as my_socket:
    my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    if len(sys.argv) == 3:
        METHOD = sys.argv[1]
    else:
        sys.exit("Usage: python3 client.py method receiver@IP:SIPport")
    try:
        USER = sys.argv[2].split("@")[0]
        IP = sys.argv[2].split("@")[1].split(":")[0]
        PORT = int(sys.argv[2].split("@")[1].split(":")[1])
        my_socket.connect((IP, PORT))
        my_socket.send(bytes(METHOD + " sip:" + USER + "@" + IP +
                             " SIP/2.0", 'utf-8') + b'\r\n\r\n')
    except IndexError:
        sys.exit("Usage: Error in -> receiver@IP:SIPport <-")

    data = my_socket.recv(1024)
    n_data = data.decode('utf-8').split()
    print(data.decode('utf-8'))

    if n_data[1] == "100" and n_data[4] == "180" and n_data[7] == "200":
        print("Send ACK, if you have to wait your request is okey")
        my_socket.send(bytes("ACK" + " sip:" + USER + "@" + IP +
                       " SIP/2.0", 'utf-8') + b'\r\n\r\n')
        data = my_socket.recv(1024)
        n_data = data.decode('utf-8').split()
        try:
            if n_data[1] == "400" or n_data[1] == "405":
                print(data.decode('utf-8'))
        except IndexError:
            pass

    print("Terminando socket...")

print("Fin.")
