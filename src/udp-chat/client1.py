#!/usr/bin/env python3

from socket import socket, AF_INET, SOCK_DGRAM  # Importamos del módulo socket la clase socket y las constantes para sockets IP y datagramas

sock = socket(AF_INET, SOCK_DGRAM)  # Creamos el socket de familia IP, tipo UDP (datagrama)
destination_address = ("localhost", 12345)  # Definimos la direccion de destino con una tupla de IP y puerto


sock.sendto(b"hello", destination_address)  # Enviamos la secuencia de bytes representada por "hello" a la dirección indicada anteriormente
sock.close()
