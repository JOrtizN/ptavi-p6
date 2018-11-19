#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import socketserver
import sys
import os

if (len(sys.argv) == 4):
    IP = sys.argv[1]
    PORT = int(sys.argv[2])
    fichero_audio = sys.argv[3]
else:
    sys.exit("Usage: python3 server.py IP port audio_file")

class EchoHandler(socketserver.DatagramRequestHandler):
    """
    Echo server class
    """

    def handle(self):
        # Escribe dirección y puerto del cliente (de tupla client_address)
    #print("Registro de clientes:")
        for line in self.rfile:
            method = line.decode('utf-8').split(" ")[0]
            if (method == "INVITE"):
                self.wfile.write(b"SIP/2.0 100 Trying SIP/2.0 180 Ringing SIP/2.0 200 OK \r\n\r\n")
                print("El cliente nos manda " + line.decode('utf-8'))

            elif (method == "ACK"):
                print("El cliente nos manda " + line.decode('utf-8'))
                aEjecutar = 'mp32rtp -i 127.0.0.1 -p 23032 < ' + fichero_audio
                print("Vamos a ejecutar", aEjecutar)
                os.system(aEjecutar)
                print("Cancion enviada")

            elif (method == "BYE"):
                print("El cliente nos manda " + line.decode('utf-8'))
                self.wfile.write(b"SIP/2.0 200 OK \r\n\r\n")

            #elif (method == "BYE"):

if __name__ == "__main__":
    # Creamos servidor de eco y escuchamos
    serv = socketserver.UDPServer((IP, PORT), EchoHandler)
    print("Listening...")
    serv.serve_forever()
