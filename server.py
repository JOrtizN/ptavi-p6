#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Clase (y programa principal) para un servidor de eco en UDP simple."""

import socketserver
import sys
import os

if len(sys.argv) == 4:
    IP = sys.argv[1]
    PORT = int(sys.argv[2])
    fich_audio = sys.argv[3]

else:
    sys.exit("Usage: python3 server.py IP port audio_file")


class EchoHandler(socketserver.DatagramRequestHandler):
    """Echo server class."""

    def handle(self):
        """Filtrar por métodos."""
        for line in self.rfile:
            llega = line.decode('utf-8').split(" ")
            method = llega[0]

            try:
                arroba = llega[1].find("@") == -1
                fsip = str(llega[1].split(":")[0]) != "sip"
                lsip = str(llega[2]) != "SIP/2.0\r\n"
                if (fsip or arroba or lsip):
                    print("SIP/2.0 400 Bad Request\r\n\r\n")
                    self.wfile.write(b"SIP/2.0 400 Bad Request\r\n\r\n")
                    break
            except IndexError:
                pass

            if len(llega) == 3:
                if method not in ['INVITE', 'BYE', 'ACK']:
                    self.wfile.write(b'SIP/2.0 405 Method Not Allowed\r\n')
                    break

                if method == "INVITE":
                    print("El cliente nos manda " + line.decode('utf-8'))
                    self.wfile.write(b"SIP/2.0 100 Trying\r\n\r\n")
                    self.wfile.write(b"SIP/2.0 180 Ringing\r\n\r\n")
                    self.wfile.write(b"SIP/2.0 200 OK\r\n\r\n")

                elif method == "ACK":
                    print("El cliente nos manda " + line.decode('utf-8'))
                    aEjecutar = 'mp32rtp -i 127.0.0.1 -p 23032 < ' + fich_audio
                    print("Vamos a ejecutar", aEjecutar)
                    os.system(aEjecutar)
                    print("Cancion enviada")

                elif method == "BYE":
                    print("El cliente nos manda " + line.decode('utf-8'))
                    self.wfile.write(b"SIP/2.0 200 OK \r\n\r\n")

            else:
                break


if __name__ == "__main__":
    # Creamos servidor de eco y escuchamos
    serv = socketserver.UDPServer((IP, PORT), EchoHandler)
    print("Listening...")
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        print("Finalizado servidor")
